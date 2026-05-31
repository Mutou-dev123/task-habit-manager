from django.db import models

# 習慣モデル
class Habit(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    # 習慣の進行状態
    STATUS_CHOICES = [
        ("draft", "下書き"),
        ("active", "実行中"),
        ("archived", "終了"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    # 習慣頻度タイプの選択
    FREQUENCY_CHOICES = [
        ("daily", "毎日"),
        ("interval", "〇日おき"),
        ("weekday", "曜日指定"),
        ("count", "回数指定"),
    ]
    frequency = models.CharField(
        max_length=10,
        choices=FREQUENCY_CHOICES,
        default="daily"
    )

    interval_days = models.PositiveIntegerField(null=True, blank=True)

    # 習慣頻度タイプ：曜日指定
    WEEKDAY_CHOICES = [
        (0, "月"),
        (1, "火"),
        (2, "水"),
        (3, "木"),
        (4, "金"),
        (5, "土"),
        (6, "日"),
    ]
    weekdays = models.JSONField(null=True, blank=True)

    # 習慣頻度タイプ：回数指定
    COUNT_TYPE_CHOICES = [
        ("week", "週"),
        ("month", "月"),
    ]
    count_type = models.CharField(max_length=10, choices=COUNT_TYPE_CHOICES, null=True, blank=True)
    target_count = models.PositiveIntegerField(null=True, blank=True)

    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        from django.core.exceptions import ValidationError
        
        # interval
        if self.frequency == "interval":
            if self.interval_days is None or self.interval_days <= 0:
                raise ValidationError("interval_daysは1以上が必要です")
        else:
                self.interval_days = None
        
        # weekday
        if self.frequency == "weekday":
            if not self.weekdays:
                raise ValidationError("weekdaysが必要です")
            if not all(isinstance(d, int) and 0 <= d <= 6 for d in self.weekdays):
                raise ValidationError("weekdaysは0～6の整数リスト")
        else:
            self.weekdays = None

        # count
        if self.frequency == "count":
            if not self.count_type:
                raise ValidationError("count_typeが必要です")
            if self.target_count is None or self.target_count <= 0:
                raise ValidationError("target_countは1以上")
            
        else:
            self.count_type = None
            self.target_count = None
        
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError("終了日は開始日より後にしてください")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

# 習慣実行ログ
class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="logs")
    date = models.DateField()

    completed_at = models.DateTimeField(auto_now_add=True)

    memo = models.TextField(blank=True)

    # 一日一回のみチェックを許可
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["habit", "date"], name="unique_habit_log")
        ]
        indexes = [
            models.Index(fields=["habit", "date"]),
        ]
        ordering = ["-date"]

# 習慣スキップ
class HabitSkip(models.Model):
    habit = models.ForeignKey("Habit", on_delete=models.CASCADE)
    date = models.DateField()

    reason = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["habit", "date"],
                name="unique_habit_skip"
            )
        ]