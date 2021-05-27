from django.urls import path

from .views import ScheduleView, UserView, StartupInfo, WeekScheduleView

urlpatterns = [
    path('schedule', ScheduleView.as_view(), name='get-schedule'),
    path('week_schedule', WeekScheduleView.as_view(), name='get-week-schedule'),
    path('user', UserView.as_view()),
    path('startup_info', StartupInfo.as_view()),
]
