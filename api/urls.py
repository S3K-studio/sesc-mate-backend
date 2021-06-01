from django.urls import path

from api import views

urlpatterns = [
    path('schedule', views.get_schedule, name='get-schedule'),
    path('week_schedule', views.get_week_schedule, name='get-week-schedule'),
    path('user', views.UserView.as_view(), name='user'),
    path('startup_info', views.get_startup_info, name='startup-info'),
]
