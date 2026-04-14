from django.shortcuts import render
from .models import Task
from django.shortcuts import get_object_or_404

def task_list(request):
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})

def task_detail(request, pk):
    task = get_object_or_404(Task, id=pk)
    return render(request, "tasks/task_detail.html", {"task": task})