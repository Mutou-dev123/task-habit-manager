from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm
from django.shortcuts import get_object_or_404

# タスク一覧
def task_list(request):
    tasks = Task.objects.all()
    return render(request, "tasks/task_list.html", {"tasks": tasks})

# タスク詳細
def task_detail(request, pk):
    task = get_object_or_404(Task, id=pk)
    return render(request, "tasks/task_detail.html", {"task": task})

# タスク作成
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {"form": form})