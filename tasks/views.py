from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

# タスク一覧
def task_list(request):
    tasks = Task.objects.exclude(status="draft")   # 下書きは一覧では非表示
    return render(request, "tasks/task_list.html", {"tasks": tasks})

# 下書きタスク一覧
def draft_list(request):
    drafts = Task.objects.filter(status="draft").order_by("-updated_at")
    return render(request, "tasks/draft_list.html", {"drafts": drafts})

# タスク詳細
def task_detail(request, pk):
    task = get_object_or_404(Task, id=pk)
    return render(request, "tasks/task_detail.html", {"task": task})

# タスク作成
def task_create(request):
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

    return render(request, "tasks/task_form.html", {"form": form})

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
        return redirect("task_list")
    
    return render(request, "tasks/task_confirm_delete.html", {"task": task})

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