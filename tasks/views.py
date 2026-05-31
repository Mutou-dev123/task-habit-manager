# タスクビュー

from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.db.models import Q, F, Case, When, Value, IntegerField
from django.core.paginator import Paginator
import time

# タスク一覧
def task_list(request):
    # 下書きを除いたすべてのタスクのベース
    all_non_draft_tasks = Task.objects.exclude(status="draft")

    # 下書き以外のタスクがDBに1件でも存在するかをチェックするフラグ
    # 検索結果が0件なのか、初期状態の0件なのかがHTML側で判断可能に
    has_tasks_at_all = all_non_draft_tasks.exists()

    # ステータスが "draft" のタスクの総数をカウント
    draft_count = Task.objects.filter(status="draft").count()

    tasks = all_non_draft_tasks

    q = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    sort = request.GET.get("sort", "").strip()

    # 検索
    if q:
        tasks = tasks.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )
    
    # フィルター
    if status:
        tasks = tasks.filter(status=status)

    # 並び替え
    if sort == "due":
        tasks = tasks.order_by("due_date", "id")
    
    elif sort == "title":
        tasks = tasks.order_by("title", "id")

    else:
        # デフォルト（ユーザーがソートを指定していない時）の並び順設定
        # doing → todo → done の順に並び変えるためのマッピング
        tasks = tasks.annotate(
            status_order=Case(
                When(status="doing", then=Value(1)),
                When(status="todo", then=Value(2)),
                When(status="done", then=Value(3)),
                output_field=IntegerField(),
            )
        )

        # 「ステータス順」かつ「更新日時が新しい順」でソート実行
        tasks = tasks.order_by("status_order", "-updated_at", "id")

    # ページネーション（無限スクロール）
    paginator = Paginator(tasks, 9) # 1ページに9個ずつに分割
    page_number = request.GET.get('page', 1)    # 何ページ目かをURLから取得（デフォルト＝1）
    page_obj = paginator.get_page(page_number)

    # JSからの「追加読み込み」要求（XMLHttpRequest）の際、
    # ページ全体ではなく、追加分のカードのHTML（部分用テンプレート）だけを返す
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and 'page' in request.GET:
        response = render(request, "tasks/task_list_partials.html", {"tasks": page_obj})

        # 次があるかの情報を載せる
        response['X-Has-Next'] = 'true' if page_obj.has_next() else 'false'

        return response
    
    context = {
        "tasks": page_obj,
        "q": q,
        "status": status,
        "sort": sort,
        "has_next": page_obj.has_next(), # 次のページがあるかどうかのフラグ
        "draft_count": draft_count,      # 下書き件数
        "has_tasks_at_all": has_tasks_at_all, # 通常タスク有無フラグ
    }

    return render(request, "tasks/task_list.html", context)

# 下書きタスク一覧
def task_draft_list(request):
    drafts = Task.objects.filter(status="draft").order_by("-updated_at")
    return render(request, "tasks/task_draft_list.html", {"drafts": drafts})

# タスク詳細
def task_detail(request, pk):
    task = Task.objects.get(id=pk)

    from_day = request.GET.get("from") == "day"

    year = request.GET.get("year")
    month = request.GET.get("month")
    day = request.GET.get("day")

    context = {
        "task": task,
        "from_day": from_day,
        "year": year,
        "month": month,
        "day": day,
    }

    return render(request, "tasks/task_detail.html", context)

# タスク作成
def task_create(request):

    draft_exists = Task.objects.filter(
        status="draft"
    ).exists()

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)

            # 作成か下書き保存かを判断
            if "save_draft" in request.POST:
                task.status = "draft"
            else:
                task.status = "todo"

            task.save()
            return redirect("task_list")
    
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {
        "form": form,
        "draft_exists": draft_exists,
    })

# タスク編集
def task_update(request, pk):
    task = get_object_or_404(Task, id=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_detail", pk=task.id)
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/task_form.html", {
        "form": form,
        "task": task,
        "mode": "edit",
    })

# タスク削除
def task_delete(request, pk):
    task = get_object_or_404(Task, id=pk)

    if request.method == "POST":
        task.delete()
        
        # JavaScriptからの削除リクエストの場合、画面遷移せず「成功した」とだけ返す
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            from django.http import JsonResponse
            return JsonResponse({"status": "success"})
    
        return redirect("task_list")
    return redirect("task_list")

# タスク完了
def task_complete(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, id=pk)
        task.status = "done"
        task.save()
    return redirect("task_list")

# タスク完了取り消し
def task_undo(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, id=pk)
        task.status = "todo"
        task.save()
    return redirect("task_list")

# ステータスワンクリック変更
def task_next_status(request, pk):
    task = get_object_or_404(Task, id=pk)

    if task.status == "todo":
        task.status = "doing"
    elif task.status == "doing":
        task.status = "done"

    task.save()
    return redirect("task_list")

# ステータスプルダウン変更
def task_update_status(request, pk):
    task = get_object_or_404(Task, id=pk)

    if request.method == "POST":
        task.status = request.POST.get("status")
        task.save()

    return redirect("task_detail", pk=task.id)