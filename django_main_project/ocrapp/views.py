from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import parsers
# Create your views here.


class PingOcrApp(GenericAPIView):

    def get(self,request, *args, **kwargs):
        """
        ping ocrapp
        """
        return Response('access')


from rest_framework import viewsets
from .models import FileServerTb, ProcessServerTb, UploadFileProcessedTb, UploadFileTb, PingTb
from .serializers import (FileServerTbSerializer, ListProcessServerTbSerializer,
                          ListUploadFileProcessedTbSerializer,
                          ListUploadFileTbSerializer, PingTbSerializer,
                          ProcessServerTbSerializer,
                          UploadFileProcessedTbSerializer,
                          UploadFileTbSerializer)


class UploadFileViewSet(viewsets.ViewSet):
    

    def list(self, request):
        queryset = UploadFileTb.objects.all()
        serializer = ListUploadFileTbSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            upload_file = UploadFileTb.objects.get(pk=pk)
        except UploadFileTb.DoesNotExist:
            return Response(status=404)
        serializer = UploadFileTbSerializer(upload_file)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def upload(self, request):
        # 这个 action 只接受 multipart/form-data
        # parser_classes 会在下面指定
        serializer = UploadFileTbSerializer(data=request.data)
        if serializer.is_valid():
            # 处理上传逻辑
            file_obj = serializer.validated_data['file']
            # ... 保存文件等操作
            return Response({'status': 'file uploaded'})
        return Response(serializer.errors)
    upload.parser_classes = [parsers.MultiPartParser, parsers.FormParser]









    






