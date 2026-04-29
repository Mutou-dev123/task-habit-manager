from django import forms
from django.contrib import admin
from .models import Habit

class HabitAdminForm(forms.ModelForm):
    weekdays = forms.MultipleChoiceField(
        choices=Habit.WEEKDAY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    def clean_weekdays(self):
        return [int(w) for w in self.cleaned_data["weekdays"]]
    
class HabitAdmin(admin.ModelAdmin):
    form = HabitAdminForm

admin.site.register(Habit, HabitAdmin)
