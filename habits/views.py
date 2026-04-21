from django.shortcuts import render, redirect ,get_list_or_404
from .models import Habit
from .forms import HabitForm

# 習慣一覧
def habit_list(request):
    habits = Habit.objects.exclude(status="draft")
    return render(request, "habits/habit_list.html", {"habits": habits})

# 下書き習慣一覧
def draft_list(request):
    drafts = Habit.objects.filter(status="draft").order_by("-updated_at")
    return render(request, "habits/habit_list.html", {"drafts": drafts})

# 習慣詳細
def habit_detail(request, pk):
    habit = get_list_or_404(Habit, id=pk)
    return render(request, "habits/habit_detail.html", {"habit": habit})

# 習慣作成
def habit_create(request):
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

    return render(request, "habits/habit_form.html", {"form": form})

# 習慣編集
def habit_update(request, pk):
    habit = get_list_or_404(Habit, id=pk)

    if request.method == "POST":
        form = HabitForm(request.POST, instance=habit)
        if form.is_valid():
            form.save()
            return render("habit_detail", pk=habit.id)
    else:
        form = HabitForm(instance=habit)

    return render(request, "habits/habit_form.html", {
        "form": form,
        "habit": habit,
        "mode": "mode",
    })

# 習慣削除
def habit_delete(request, pk):
    habit = get_list_or_404(Habit, id=pk)

    if request.method == "POST":
        habit.delete()
        return redirect("habit_list")
    
    return render(request, "habits/habit_confirm_delete.html", {"habit": habit})