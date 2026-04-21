from django.urls import path
from . import views

urlpatterns = [
    path("", views.habit_list, name="habit_list"),
]