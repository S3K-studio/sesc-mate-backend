from django.urls import path

from .views import *


urlpatterns = [
    path('', AliceView.as_view())
]
