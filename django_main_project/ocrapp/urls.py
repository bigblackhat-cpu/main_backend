from django.urls import path
from .views import (
    PingOcrApp
)

urlpatterns = [
    path('ping/',PingOcrApp.as_view())
]