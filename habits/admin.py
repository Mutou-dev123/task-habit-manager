from django import forms
from django.contrib import admin
from .models import Habit, HabitLog

# Habit用の「管理画面フォーム」をカスタマイズするクラス

# ここではweekdaysがJSONFieldでそのままだとadminで、
# [0, 2, 4] のように表示されてしまう
class HabitAdminForm(forms.ModelForm):

    # 選択可能なフォーム項目
    weekdays = forms.MultipleChoiceField(

        # モデルHabitクラスのWEEKDAY_CHOICESを使用
        choices=Habit.WEEKDAY_CHOICES,

        # どう表示するかを指定。今回はチェックボックス形式
        widget=forms.CheckboxSelectMultiple,

        # 未選択OK
        required=False
    )

    class Meta:
        model = Habit   # Habitモデル用フォーム
        fields = "__all__"  # 全フィールドをフォームに含める

    # weekdays専用のバリデーション/変換処理
    def clean_weekdays(self):
        weekdays = self.cleaned_data.get("weekdays")    # チェックされた曜日取得
        # self.cleaned_data ... 
    
        if not weekdays:
            return None
        
        return [int(w) for w in weekdays]

class HabitLogInline(admin.TabularInline):
    model = HabitLog
    extra = 0   # 空フォームを無駄に表示しない

# @ ... クラスや関数に追加機能をくっつける

@admin.register(Habit)  # HabitAdminをHabitモデルに追加
class HabitAdmin(admin.ModelAdmin):
    form = HabitAdminForm

    # 一覧画面に表示する列
    list_display = (
        "title",
        "frequency",
        "status",
        "start_date",
        "end_date",
        "created_at",
    )

    # 右側にフィルタ追加
    list_filter = (
        "status",
        "frequency",
    )

    # 検索バー
    search_fields = (
        "title",
        "description",
    )

    # 親画面でモデル編集
    inlines = [HabitLogInline]  # Habit詳細画面内でHabitLogも編集可能に

@admin.register(HabitLog)   # HabitLogAdminをHabitLogに追加
class HabitLogAdmin(admin.ModelAdmin):

    # 一覧画面に表示する列
    list_display = (
        "habit",
        "date",
        "completed_at",
    )

    # 右側にフィルタ追加
    list_filter = (
        "date",
    )

    # 検索バー
    search_fields = (
        "habit__title",
    )

    # 日付ナビ
    date_hierarchy = "date" # 管理画面上部にナビゲーション「年、月、日」が表示される

# ModelAdminオプション
# ・list_display
# ・list_filter
# ・search_fields
# ・date_hierarchy
# ・inlines