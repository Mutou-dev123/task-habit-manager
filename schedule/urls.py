from django.urls import path
from . import views

urlpatterns = [
    path("", views.calendar_view, name="calendar_view"),
    path(
        "day/<int:year>/<int:month>/<int:day>/",
        views.day_detail,
        name="day_detail",
    )
]