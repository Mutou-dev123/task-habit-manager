from django.urls import path
from . import views

urlpatterns = [
    path("", views.habit_list, name="habit_list"),
    path("<int:pk>/", views.habit_detail, name="habit_detail"),
    path("create/", views.habit_create, name="habit_create"),
    path("<int:pk>/edit/", views.habit_update, name="habit_update"),
    path("<int:pk>/delete/", views.habit_delete, name="habit_delete"),
    path("drafts/", views.draft_list, name="draft_list"),
]