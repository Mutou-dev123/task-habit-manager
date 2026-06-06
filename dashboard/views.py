# ダッシュボードビュー

from django.shortcuts import render
from django.utils import timezone

from tasks.models import Task
from habits.models import Habit
from django.db.models import Q

def home(request):
    today = timezone.now().date()

    tasks = Task.objects.filter(
        due_date=today
    ).exclude(
        status__in=["done", "draft"]
    )

    today_items = []

    for task in tasks:

        today_items.append({
            "type": "task",
            "title": task.title,
            "obj": task
        })

    habits = Habit.objects.filter(
        status="active",
        start_date__lte=today
    ).filter(
        Q(end_date__isnull=True) |
        Q(end_date__gte=today)
    )

    for habit in habits:

        today_items.append({
            "type": "habit",
            "title": habit.title,
            "obj": habit,
        })

    return render(request, "dashboard/home.html", {"today_items": today_items,})