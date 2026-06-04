import calendar # カレンダー
from datetime import date, datetime, timedelta
from collections import defaultdict # dict（辞書）の拡張モジュール

from django.shortcuts import render
from tasks.models import Task
from habits.models import Habit, HabitLog, HabitSkip
from habits.services import HabitService

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
        date__year=year,
        date__month=month
    ).values("habit_id", "date")

    # 日付ごとにまとめる
    task_dict = defaultdict(list)
    for task in tasks:
        task_dict[task.due_date.day].append(task)

    habit_dict = defaultdict(list)
    
    log_set = set(
        (log["habit_id"], log["date"].day)
        for log in logs
    )
    
    for week in cal:
        for day in week:

            if day == 0:
                continue

            current_date = date(year, month, day)

            for habit in habits:
                
                # その日にやるべき習慣かチェック
                if HabitService.is_scheduled_for(habit, current_date):

                    # 完了済み判定（上で作った log_set を使い回すだけ！）
                    is_done = (habit.id, day) in log_set

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

    current_date = date(
        int(year),
        int(month),
        int(day)
    )

    prev_date = current_date - timedelta(days=1)
    next_date = current_date + timedelta(days=1)

    tasks = Task.objects.filter(
        due_date=current_date
    ).exclude(
        status="draft"
    )

    habit_states = (
        HabitService.get_habit_states(
            current_date
        )
    )

    context = {
        "current_date": current_date,

        "prev_year": prev_date.year,
        "prev_month": prev_date.month,
        "prev_day": prev_date.day,

        "next_year": next_date.year,
        "next_month": next_date.month,
        "next_day": next_date.day,

        "tasks": tasks,
        "habit_states": habit_states,
    }

    return render(
        request,
        "schedule/day_detail.html",
        context
    )