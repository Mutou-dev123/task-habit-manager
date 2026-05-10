from django import forms
from .models import Task
from datetime import date

# タスク作成フォーム
class TaskForm (forms.ModelForm):
    
    class Meta:
        model = Task

        fields = [
            "title",
            "description",
            "due_date",
            "link",
        ]

        labels = {
            "title": "タイトル",
            "description": "詳細",
            "due_date": "期限日",
            "link": "関連リンク",
        }

        widgets = {

            # タイトル
            "title": forms.TextInput(
                attrs={
                    "placeholder": "例：レポート提出",
                }
            ),

            # 詳細
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "メモや補足を書く",
                }
            ),

            # 日付入力
            "due_date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),

            # URL
            "link": forms.URLInput(
                attrs={
                    "placeholder": "https://...",
                }
            ),
        }