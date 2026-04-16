from django.urls import path
from . import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path("<int:pk>/", views.task_detail, name="task_detail"),
    path("create/", views.task_create, name="task_create"),
    path("<int:pk>/edit/", views.task_update, name="task_update"),
    path("<int:pk>/delete/", views.task_delete, name="task_delete"),
    path("<int:pk>/complete/", views.task_complete, name="task_complete"),
    path("<int:pk>/undo/", views.task_undo, name="task_undo"),
    path("<int:pk>/next/", views.task_next_status, name="task_next_status"),
    path("<int:pk>/status/", views.task_update_status, name="task_update_status"),
]