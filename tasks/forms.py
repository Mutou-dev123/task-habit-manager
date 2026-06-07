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
            'color',
        ]

        labels = {
            "title": "タイトル",
            "description": "メモ",
            "due_date": "期限日",
            "link": "関連リンク",
            "color": "カラー",
        }

        widgets = {

            # タイトル
            "title": forms.TextInput(
                attrs={
                    "placeholder": "例：レポート提出",
                    "maxlength": "50",
                }
            ),

            # メモ
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "メモや補足を書く",
                    "maxlength": "500",
                }
            ),

            # 期限日
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

            # カラー
            "color": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),
        }