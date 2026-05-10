from django import forms
from .models import Habit
from datetime import date

# 習慣作成フォーム
class HabitForm(forms.ModelForm):
    WEEKDAY_CHOICES = [
        (0, "月"), (1, "火"), (2, "水"), (3, "木"), (4, "金"), (5, "土"), (6, "日"),
    ]

    weekdays = forms.MultipleChoiceField(
        choices=WEEKDAY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="曜日指定"
    )

    class Meta:
        model = Habit

        fields = [
            "title", "description", "start_date", "end_date",
            "frequency", "interval_days", "weekdays",
            "count_type", "target_count", "link",
        ]

        labels = {
            "title": "タイトル",
            "description": "詳細",
            "start_date": "開始日",
            "end_date": "終了日",
            "frequency": "習慣頻度",
            "interval_days": "間隔日数",
            "count_type": "カウント単位",
            "target_count": "目標回数",
            "link": "関連リンク",
        }

        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 編集時の曜日初期化
        if self.instance and self.instance.weekdays:
            self.initial["weekdays"] = self.instance.weekdays

        # 作成時の開始日を今日に設定
        if not self.instance.pk:
            self.initial["start_date"] = date.today()

    def clean_weekdays(self):
        weekdays = self.cleaned_data.get("weekdays")
        
        if not weekdays:
            return None
        
        return [int(w) for w in weekdays]