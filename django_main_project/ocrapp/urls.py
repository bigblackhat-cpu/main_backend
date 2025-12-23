from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    PingOcrApp,
    UploadFileViewSet
)
router = DefaultRouter()
router.register(r'upload-file', UploadFileViewSet, basename='upload-file')  # 如果它是 ViewSet

urlpatterns = [
    path('ping/',PingOcrApp.as_view())

]

urlpatterns += router.urls