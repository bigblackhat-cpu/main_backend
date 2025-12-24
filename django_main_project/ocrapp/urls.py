from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UploadFileViewSet,
    UploadFileProcessedViewSet,
    ProcessServerModelViewSet,
    FileServerGenericViewSet
)
router = DefaultRouter()
router.register(r'upload_file', UploadFileViewSet, basename='upload_file')  # 如果它是 ViewSet
router.register(r'processed_file_upload',UploadFileProcessedViewSet, basename='processed_file_upload')
router.register(r'third_server',ProcessServerModelViewSet, basename='third_server')
router.register(r'process_task',FileServerGenericViewSet,basename='process_task')

urlpatterns = [
    

]

urlpatterns += router.urls