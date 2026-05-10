import calendar # カレンダー
from datetime import date
from collections import defaultdict # dict（辞書）の拡張モジュール

from django.shortcuts import render
from tasks.models import Task
from habits.models import Habit, HabitLog

# カレンダー
def calendar_view(request):
    today = date.today()

    # GETパラメータ取得
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))

    mode = request.GET.get("mode", "all")

    cal = calendar.monthcalendar(year, month)

    # 前月
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year -=1

    # 次月
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

    habits = Habit.objects.filter(status="active")

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
    
    for week in cal:
        for day in week:

            if day == 0:
                continue

            current_date = date(year, month, day)

            for habit in habits:

                if habit.is_scheduled_for(current_date):

                    # 完了済み判定
                    is_done = logs.filter(
                        habit=habit,
                        date=current_date
                    ).exists()

                    habit_dict[day].append({
                        "habit": habit,
                        "is_done": is_done,
                    })

    context = {
        "calendar": cal,
        "year": year,
        "month": month,
        "today": today,
        "prev_year": prev_year,
        "prev_month": prev_month,
        "next_year": next_year,
        "next_month": next_month,
        "task_dict": dict(task_dict),
        "habit_dict": dict(habit_dict),
        "mode": mode,
    }

    return render(request, "schedule/calendar.html", context)

# 日別詳細
def day_detail(request, year, month, day):
    
    target_date = date(year, month, day)

    tasks = Task.objects.filter(
        due_date=target_date
    ).exclude(
        status="draft"
    )

    # 習慣取得
    habits = Habit.objects.filter(
        status="active"
    )

    # その日に予定されている習慣
    scheduled_habits = [
        habit for habit in habits
        if habit.is_scheduled_for(target_date)
    ]

    # 完了済みログ
    logs = HabitLog.objects.filter(
        date=target_date
    )

    # 完了済み習慣ID
    done_habit_ids = set(
        log.habit_id for log in logs
    )

    context = {
        "target_date": target_date,
        "tasks": tasks,
        "scheduled_habits": scheduled_habits,
        "done_habit_ids": done_habit_ids,
    }

    return render(
        request,
        "schedule/day_detail.html",
        context
    )