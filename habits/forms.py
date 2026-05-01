from django import forms
from .models import Habit

# 習慣作成フォーム
class HabitForm(forms.ModelForm):
    WEEKDAY_CHOICES = [
        (0, "月"), (1, "火"), (2, "水"), (3, "木"), (4, "金"), (5, "土"), (6, "日"),
    ]

    weekdays = forms.MultipleChoiceField(
        choices=WEEKDAY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="実施曜日"
    )

    class Meta:
        model = Habit
        fields = [
            "title", "description", "start_date", "end_date",
            "frequency", "interval_days", "weekdays",
            "count_type", "target_count", "link",
        ]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.weekdays:
            self.initial["weekdays"] = self.instance.weekdays

    def clean_weekdays(self):
        data = self.cleaned_data.get("weekdays")
        if data:
            return [int(d) for d in data]
        return None