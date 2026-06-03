from django.contrib import admin
from .models import Task

@admin.register(Task)   # TaskAdminをTaskに追加
# Task用の「管理画面フォーム」をカスタマイズするクラス
class TaskAdmin(admin.ModelAdmin):

    # 一覧画面に表示する列
    list_display = (
        "title",
        "status",
        "due_date",
        "created_at",
    )

    # 右側にフィルタ追加
    list_filter = (
        "status",
        "due_date",
        "created_at",
    )

    # 検索バー
    search_fields = (
        "title",
        "description",
    )

    # 作成日降順
    # 管理者画面のみの並べ替えも可能
    ordering = (
        "-created_at",
    )

    # 日付ナビ
    date_hierarchy = "due_date"

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    # フォームのグループ分け
    fieldsets = (
        (
            "基本情報",
            {
                "fields": (
                    "title",
                    "description",
                    "status",
                )
            }
        ),
        (
            "期限・リンク",
            {
                "fields": (
                    "due_date",
                    "link",
                )
            }
        ),
        (
            "システム情報",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            }
        ),
    )