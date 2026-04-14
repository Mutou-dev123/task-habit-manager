from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('', include('dashboard.urls')),
=======
>>>>>>> 21e44e8827c243ecd0449910ae13b0a00964a9e7
    path('tasks/', include('tasks.urls')),
    path('habits/', include('habits.urls')),
]