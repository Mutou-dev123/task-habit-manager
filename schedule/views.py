import calendar # カレンダー
from datetime import date
from collections import defaultdict # dict（辞書）の拡張モジュール

from django.shortcuts import render
from tasks.models import Task
from habits.models import HabitLog

# カレンダー
def calendar_view(request):
    today = date.today()

    # GETパラメータ取得
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    cal = calendar.monthcalendar(year, month)

    # 前月・次月計算
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -=1

    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year += 1
    
    # タスク取得
    tasks = Task.objects.exclude(
        status="draft"
    ).filter(
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
        task_dict[task.due_date.day].append(task)

    habit_dict = defaultdict(list)
    for log in logs:
        habit_dict[log.date.day].append(log)

    print(year, month)
    print(tasks)

    context = {
        "calendar": cal,
        "year": year,
        "month": month,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
        "task_dict": dict(task_dict),
        "habit_dict": dict(habit_dict),
    }

    return render(request, "schedule/calendar.html", context)