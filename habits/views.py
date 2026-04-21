from django.shortcuts import render, redirect ,get_list_or_404
from .models import Habit

# 習慣一覧
def habit_list(request):
    habits = Habit.objects.all()
    return render(request, "habits/habit_list.html")