from django.shortcuts import render
from tasks.models import Task
from django.utils import timezone

def home(request):
    today = timezone.now().date()
    print(today)

    tasks = Task.objects.filter(due_date=today)

    return render(request, "dashboard/home.html", {"tasks": tasks})