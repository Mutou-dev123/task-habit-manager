from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm

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

# タスク編集
def task_update(request, pk):
    task = get_object_or_404(Task, id=pk)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/task_form.html", {"form": form})

# タスク削除
def task_delete(request, pk):
    task = get_object_or_404(Task, id=pk)

    if request.method == "POST":
        task.delete()
        return redirect("task_list")
    
    return render(request, "tasks/task_confirm_delete.html", {"task": task})