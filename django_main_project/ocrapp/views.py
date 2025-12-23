from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import parsers
from rest_framework import status

# Create your views here.


from rest_framework import viewsets
from .models import (
    FileServerTb,
    ProcessServerTb,
    UploadFileProcessedTb,
    UploadFileTb,
)
from .serializers import (
    ListUploadFileTbSerializer,
    UploadFileTbRetrieveSerializer,
    UploadFileTbSerializer,
    ProcessServerTbSerializer,
)


class UploadFileViewSet(viewsets.GenericViewSet):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get_serializer_class(self):
        if self.action == "list":
            return ListUploadFileTbSerializer
        elif self.action == "retrieve":
            return UploadFileTbRetrieveSerializer
        elif self.action == "create":
            return UploadFileTbSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return UploadFileTb.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            extra_data = {
                "user_id": 1,
                "filename": serializer.validated_data["file"].name,
                "file_type": serializer.validated_data["file"].content_type,
            }
            instance = serializer.save(**extra_data)
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

from .serializers import(
    UploadFileProcessedTbSerializer,
    ListUploadFileProcessedTbSerializer
)
class UploadFileProcessedViewSet(viewsets.GenericViewSet):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get_serializer_class(self):
        if self.action == 'create':
            return UploadFileProcessedTbSerializer
        elif self.action == 'list':
            return ListUploadFileProcessedTbSerializer
        elif self.action == 'retrieve':
            return 
        return ListUploadFileProcessedTbSerializer
    
    def get_queryset(self):
        return UploadFileProcessedTb.objects.all()
    
    def create(self,request):
        # serializer = UploadFileProcessedTbSerializer(data=request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            extra_data = {
                'processed_file_type':serializer.validated_data['processed_file'].content_type
            }
            serializer.save(**extra_data)
            return Response(serializer.data,status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
    
    def list(self,request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(data=queryset,many=True)
        return Response(serializer.data,status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            upload_file = UploadFileTb.objects.get(pk=pk)
        except UploadFileTb.DoesNotExist:
            return Response(status=404)
        serializer = UploadFileTbSerializer(upload_file)
        return Response(serializer.data)
            



from rest_framework import generics


class ListProcessServerAPIView(generics.ListAPIView):
    """
    list thiry server , now we have，可以ping一下第三方服务
    """

    serializer_class = ProcessServerTbSerializer
    queryset = ProcessServerTb.objects.all()


class ListFileServerTb(generics.GenericAPIView):
    def get(self, request):
        """
        Docstring for post

        返回在redis中，的任务,如果有任务正在计算或pending，如果没有没有计算过或者已经计算结束
        """
        return

    def post(self, request):
        """
        Docstring for post

        发起一个对ocr第三方服务器的请求，要进行提前的判断，任务是否在redis中，
        """
