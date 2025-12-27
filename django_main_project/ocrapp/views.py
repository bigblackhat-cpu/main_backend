from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import parsers
from rest_framework import status

# Create your views here.


from rest_framework import viewsets
from .models import (
    UploadFileProcessedTb,
    UploadFileTb,
)
from .serializers import (
    ListUploadFileTbSerializer,
    UploadFileTbRetrieveSerializer,
    UploadFileTbSerializer,
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
            return ListUploadFileProcessedTbSerializer
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
            

from .serializers import (
    ProcessServerTbSerializer
)
from .models import (
    ProcessServerTb
)
from drf_spectacular.utils import extend_schema, OpenApiResponse
class ProcessServerModelViewSet(viewsets.ModelViewSet):
    """
    除了crud ，还有个，ping 通功能
    list thiry server , now we have，可以ping一下第三方服务,第三方服务的crud
    """
    queryset = ProcessServerTb.objects.all()
    serializer_class = ProcessServerTbSerializer


    @extend_schema(
        # 自定义接口描述
        description="Ping第三方服务器接口",
        # 定义响应结构
        responses={
            200: OpenApiResponse(
                description="Ping完成",
                # 显式指定响应结构
                response={
                    'type': 'object',
                    'properties': {
                        'status': {'type': 'string', 'example': 'ping is over'}
                    }
                }
            )
        },
        # 移除默认的请求序列化器（如果不需要）
        request=None
    )
    @action(detail=True,methods=['get'],)
    def ping_third_server(self, request, pk=None):
        # serializer=ProcessServerTbSerializer(data=request.data)
        processServer = self.get_object()
        # serializer = self.get_serializer(data=request.data)
        # if serializer.is_valid():
        response = requests.get(
            url=processServer.server_backend,
        )

        response.status_code
        print(
             response.json()
        )
       

        print(f'ping: third server : {response.json} ....')

        return Response({'status':'ping is over'})

            

"""
前端拿到taskid可以，轮询拿状态，也可以主动拿状态
l:返回redis中的全部任务。
c:接受文件id 第三方服务id，在数据库中查询数据，将数据发送到第三方服务，接受响应，判断响应，redis缓存正确响应的file-id server-id  task-id。
r:more inform in redis，前端使用taskid，直接对backend发起请求？
u:-
d:能够删除未在计算中的任务

"""
from .serializers import FileServerTbSerializer
from .models import UploadFileTb,ProcessServerTb
from django.shortcuts import get_object_or_404
import requests
from django_redis import get_redis_connection
from redis import Redis
class FileServerGenericViewSet(viewsets.GenericViewSet):
    def get_serializer_class(self):
        return FileServerTbSerializer
    def get_queryset(self):
        return 
    
    def create(self,request):
        # serializer = FileServerTbSerializer(data=request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            file_id = serializer.validated_data['upload_file_tb']
            process_server_id = serializer.validated_data['process_server_tb']
            instance_file = get_object_or_404(UploadFileTb,pk=file_id)
            instance_server = get_object_or_404(ProcessServerTb,pk=process_server_id)
            try:
                third_response =requests.post(
                    url=instance_server.server_backend,
                    json={
                        'image_url':instance_file.file
                    }
                )

                """通过third_response，得到task_id，将file_id process_server_id task_id 存到redis"""
                
                # task_id = None

                # redis_client: Redis = get_redis_connection('task_cache')
                # redis_client.set(
                #     name=f'{file_id}:{process_server_id}',
                #     value=task_id,
                #     ex=30,
                # )
                return Response('success',status=status.HTTP_200_OK)

            except Exception as e:
                return Response(e)
        else:
            Response(serializer.errors)


    def list(self,request):
        """通过request的json,查询范围内的k-v,通过指定的数据库和前缀查值"""

class TaskStatusGenericAPIView(GenericAPIView):
    def post(self,request):
        serializer = FileServerTbSerializer(request.data)
        if serializer.is_valid():
            file_id = serializer.validated_data['upload_file_tb']
            server_id = serializer.validated_data['process_server_tb']
            "通过file_id，server_id在redis中取出taskid，用taskid 取backend中task的具体任务状态，再序列化成json提供给前端"
        

class TaskDestroyGenericAPIView(GenericAPIView):
    def delete(self,request):
        serializer = FileServerTbSerializer(request.data)
        if serializer.is_valid():
            file_id = serializer.validated_data['upload_file_tb']
            server_id = serializer.validated_data['process_server_tb']
            "通过file_id，server_id在redis中取出taskid，用taskid 取backend中task的具体任务状态，判断状态，队列中可删除，计算中不可删除，已经完成不可删除由系统自动删除"

    





            
            

