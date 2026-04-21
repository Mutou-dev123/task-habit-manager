from django.db import models

class Habit(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    STATUS_CHOICES = [
        ("draft", "下書き"),
        ("active", "実行中"),
        ("archived", "終了"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    date = models.DateField()

    # 一日一回のみチェックを許可
    class Meta:
        unique_together = ("habit", "date")