from django import forms
from django.contrib import admin
from .models import Habit, HabitLog

class HabitAdminForm(forms.ModelForm):
    weekdays = forms.MultipleChoiceField(
        choices=Habit.WEEKDAY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Habit
        fields = "__all__"

    def clean_weekdays(self):
        weekdays = self.cleaned_data.get("weekdays")
    
        if not weekdays:
            return None

class HabitLogInline(admin.TabularInline):
    model = HabitLog
    extra = 0

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    form = HabitAdminForm

    list_display = (
        "title",
        "frequency",
        "status",
        "start_date",
        "end_date",
        "created_at",
    )

    list_filter = (
        "status",
        "frequency",
    )

    search_fields = (
        "title",
        "description",
    )

    inlines = [HabitLogInline]

@admin.register(HabitLog)
class HabitLogAdmin(admin.ModelAdmin):

    list_display = (
        "habit",
        "date",
        "completed_at",
    )

    list_filter = (
        "date",
    )

    search_fields = (
        "habit__title",
    )

    date_hierarchy = "date"
