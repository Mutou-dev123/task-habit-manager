from django import forms
from .models import Habit

# 習慣作成フォーム
class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ["title", "description", "start_date", "end_date", "link"]