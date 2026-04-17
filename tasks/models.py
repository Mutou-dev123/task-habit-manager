from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    STATUS_CHOICES = [
        ("draft", "下書き"),
        ("todo", "未着手"),
        ("doing", "進行中"),
        ("done", "完了"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.status})"
    
    # 新しいタスク順
    class Meta:
        ordering = ["-created_at"]
    # .order_by()を毎回書かなくてよくなる