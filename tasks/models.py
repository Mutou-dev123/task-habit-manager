from django.db import models

class Tasks(models.Model):
    task_name = models.CharField(max_length=50)
    task_desc = models.CharField(max_length=300)