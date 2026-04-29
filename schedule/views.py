import calendar # カレンダー
from datetime import date
from collections import defaultdict # dict（辞書）の拡張モジュール

from django.shortcuts import render
from tasks.models import Task
from habits.models import HabitLog

# カレンダー
def calendar_view(request):
    today = date.today()

    year = today.year
    month = today.month

    cal = calendar.monthcalendar(year, month)

    # タスク取得
    tasks = Task.objects.filter(
        status="todo",
        due_date__isnull=False,
        due_date__year=year,
        due_date__month=month
    )

    # 習慣ログ取得
    logs = HabitLog.objects.filter(
        date__isnull=False,
        date__year=year,
        date__month=month
    )

    # 日付ごとにまとめる
    task_dict = defaultdict(list)
    for task in tasks:
        if not task.due_date:
            continue
        task_dict[task.due_date.day].append(task)

    habit_dict = defaultdict(list)
    for log in logs:
        habit_dict[log.date.day].append(log)

    return render(request, "schedule/calendar.html", {
        "calendar": cal,
        "task_dict": dict(task_dict),
        "habit_dict": dict(habit_dict),
        "today": today,
    })