from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    ListProcessServerAPIView,
    UploadFileViewSet
)
router = DefaultRouter()
router.register(r'upload-file', UploadFileViewSet, basename='upload-file')  # 如果它是 ViewSet

urlpatterns = [
    path('process_server/',ListProcessServerAPIView.as_view())

]

urlpatterns += router.urls