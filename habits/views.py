# 習慣ビュー

from django.shortcuts import render, redirect, get_object_or_404
from .models import Habit, HabitLog, HabitSkip
from .forms import HabitForm
from datetime import date, timedelta
from django.db.models import Q

# 習慣一覧
def habit_list(request):
    today = date.today()

    habits = Habit.objects.exclude(
        status="draft"
    )

    # 今日のログ
    logs = HabitLog.objects.filter(date=today)

    done_habit_ids = set(
        logs.values_list(
            "habit_id",
            flat=True
        )
    )

    # 検索
    q = request.GET.get("q", "").strip()

    if q:
        habits = habits.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )

    # 実施状態
    state = request.GET.get("state", "").strip()

    if state == "done":

        habits = habits.filter(
            id__in=done_habit_ids
        )

    elif state == "not_done":

        habits = habits.exclude(
            id__in=done_habit_ids
        )

    # 並び替え
    sort = request.GET.get("sort", "").strip()

    if sort == "title":
        habits = habits.order_by("title")

    elif sort == "old":
        habits = habits.order_by("created_at")

    else:
        habits = habits.order_by("-created_at")

    return render(request, "habits/habit_list.html", {
        "habits": habits,
        "done_habit_ids": done_habit_ids,
        "q": q,
        "state": state,
        "sort": sort,
    })

# 下書き習慣一覧
def habit_draft_list(request):
    drafts = Habit.objects.filter(status="draft").order_by("-updated_at")
    return render(request, "habits/habit_draft_list.html", {"habits": drafts})

# 習慣詳細
def habit_detail(request, pk):
    
    habit = get_object_or_404(
        Habit,
        pk=pk
    )

    from_day = request.GET.get("from") == "day"

    year = request.GET.get("year")
    month = request.GET.get("month")
    day = request.GET.get("day")

    context = {
        "habit": habit,
        "from_day": from_day,
        "year": year,
        "month": month,
        "day": day,
    }

    return render(request, "habits/habit_detail.html", context)

# 習慣作成
def habit_create(request):

    draft_exists = Habit.objects.filter(
        status="draft"
    ).exists()

    if request.method == "POST":
        form = HabitForm(request.POST)

        if form.is_valid():
            habit = form.save(commit=False)

            if "save_draft" in request.POST:
                habit.status = "draft"
            else:
                habit.status = "active"

            habit.save()
            return redirect("habit_list")
        
    else:
        form = HabitForm()

    return render(request, "habits/habit_form.html", {
        "form": form,
        "draft_exists": draft_exists,
        })

# 習慣編集
def habit_update(request, pk):
    habit = get_object_or_404(Habit, pk=pk)

    if request.method == "POST":
        form = HabitForm(request.POST, instance=habit)
        
        if form.is_valid():
            form.save()
            return redirect("habit_detail", pk=habit.id)
    else:
        form = HabitForm(instance=habit)

    return render(
        request,
        "habits/habit_form.html",
        {"form": form}
    )

# 習慣削除
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk)

    if request.method == "POST":
        habit.delete()
        return redirect("habit_list")
    
    return render(request, "habits/habit_confirm_delete.html", {"habit": habit})

# 習慣記録
def habit_check(request, pk):
    habit = get_object_or_404(
        Habit,
        pk=pk
    )
    today = date.today()

    HabitLog.objects.get_or_create(
        habit=habit,
        date=today
    )

    if habit.frequency == "interval":

        habit.next_run_date = (
            today + timedelta(days=habit.interval_days)
        )

        habit.save()

    return redirect("habit_list")

# 習慣記録取り消し
def habit_uncheck(request, pk):
    habit = get_object_or_404(
        Habit,
        pk=pk
    )
    today = date.today()

    HabitLog.objects.filter(
        habit=habit,
        date=today
    ).delete()

    return redirect("habit_list")

# ステータスプルダウン変更
def habit_update_status(request, pk):
    habit = get_object_or_404(Habit, id=pk)

    if request.method == "POST":
        habit.status = request.POST.get("status")
        habit.save()

    return redirect("habit_detail", pk=habit.id)

# 習慣スキップ
def habit_skip(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    today = date.today()

    HabitSkip.objects.get_or_create(
        habit=habit,
        date=today
    )

    # 習慣を完了した記録を消す
    HabitLog.objects.filter(
        habit=habit,
        date=today
    ).delete()

    return redirect("habit_list")

# 習慣スキップ解除
def habit_unskip(request, pk):
    habit = get_object_or_404(Habit, pk=pk)
    today = date.today()

    # 習慣をスキップした記録を消す
    HabitSkip.objects.filter(
        habit=habit,
        date=today
    ).delete()

    return redirect("habit_list")