from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
# Create your views here.


class PingOcrApp(GenericAPIView):

    def get(self,request, *args, **kwargs):
        """
        ping ocrapp
        """
        return Response('access')


from rest_framework.parsers import MultiPartParser
from .serializers import UploadFileTbSerializer
class UploadFileView(GenericAPIView):
    parser_classes=['MultiPartParser']
    serializer_class=UploadFileTbSerializer
    def post(self,request, *args, **kwargs):
        """
        upload file ocrapp
        """
        return Response('upload file')

from rest_framework import generics
from .serializers import ListUploadFileTbSerializer
from .models import UploadFileTb
class ListUploadFileView(generics.ListAPIView):
    """
    list select file
    """
    serializer_class=ListUploadFileTbSerializer
    queryset=UploadFileTb.objects.all()

from .serializers import ListProcessServerTbSerializer
from .models import ProcessServerTb
class ListProcessServerView(generics.ListAPIView):
    """
    Docstring for ListProcessServerView
    list select process server
    """
    serializer_class=ListProcessServerTbSerializer
    queryset=ProcessServerTb.objects.all()

from .serializers import FileServerTbSerializer
from .models import FileServerTb
class CreateFileServerView(generics.CreateAPIView):
    """
    Docstring for ListFileServerView

    1.目的：可以选择一个文件，和对应的处理服务器，
    2.生成一个文件-服务器对应关系记录
    3.对第三方服务发起请求，得到task_id
    4.file_id-server_id : task_id 存到redis
    5.返回task_id,或者是提交处理的信息给前端
    """
    serializer_class=FileServerTbSerializer

from .serializers import UploadFileProcessedTbSerializer
from .models import UploadFileProcessedTb
class UploadFileProcessedView(GenericAPIView):
    """
    上传处理完毕后的文件
    """
    parser_classes = ['MultiPartParser']
    serializer_class = UploadFileProcessedTbSerializer
    def post(self,request, *args, **kwargs):
        return Response('upload processed file')

from .serializers import ListUploadFileProcessedTbSerializer
from .models import UploadFileProcessedTb
class ListUploadFileProcessedView(generics.ListAPIView):
    """
    列出处理完毕后的文件
    """
    serializer_class=ListUploadFileProcessedTbSerializer
    queryset=UploadFileProcessedTb.objects.all()






    






