from django.shortcuts import render, redirect, get_object_or_404
from .models import Habit, HabitLog
from .forms import HabitForm
from datetime import date

# 習慣一覧
def habit_list(request):
    today = date.today()
    habits = [
        habit for habit in Habit.objects.filter(status="active")
        if habit.is_scheduled_for(today)
    ]

    logs = HabitLog.objects.filter(date=today)
    done_habits_ids = set(log.habit_id for log in logs)

    return render(request, "habits/habit_list.html", {
        "habits": habits,
        "done_habit_ids": done_habits_ids,
    })

# 下書き習慣一覧
def habit_draft_list(request):
    drafts = Habit.objects.filter(status="draft").order_by("-updated_at")
    return render(request, "habits/habit_draft_list.html", {"habits": drafts})

# 習慣詳細
def habit_detail(request, pk):
    
    habit = Habit.objects.get(id=pk)

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
    ).exists

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
    habit = Habit.objects.get(pk=pk)
    today = date.today()

    HabitLog.objects.get_or_create(
        habit=habit,
        date=today
    )

    return redirect("habit_list")

# 習慣記録取り消し
def habit_uncheck(request, pk):
    habit = Habit.objects.get(pk=pk)
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