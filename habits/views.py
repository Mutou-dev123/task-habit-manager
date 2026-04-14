from django.shortcuts import render

def home(request):
    return render(request, "habits/habit_list.html")