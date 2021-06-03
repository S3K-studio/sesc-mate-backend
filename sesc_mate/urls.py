from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v2/', include('api.urls')),
    path('api/v2/bot/', include('notification_bot.urls')),
    path('api/v2/alice/', include('alice.urls'))
]
