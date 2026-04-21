from django import forms
from .models import Task

# タスク作成フォーム
class TaskForm (forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "link"]