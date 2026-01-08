from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import parsers
from rest_framework import status
# from .until.Response import success_response,error_response
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

from rest_framework.pagination import PageNumberPagination

class UploadFileViewSet(viewsets.GenericViewSet):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
    pagination_class = PageNumberPagination
   
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
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(data=page, many=True)
            serializer.is_valid()
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(data=queryset,many=True)
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
    pagination_class = PageNumberPagination

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

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(data=page,many=True)
            serializer.is_valid()
            return self.get_paginated_response(serializer.data)
        
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
        processServer = self.get_object()
        try:
            response = requests.get(
                url=processServer.server_backend,
            )
            return Response({'code':200,'status':response.json()})
        except Exception as e:
            return Response({'code':400,'msg':'ping error'}) 

from .serializers import FileServerTbSerializer
from .models import UploadFileTb,ProcessServerTb
from django.shortcuts import get_object_or_404
import requests
from django_redis import get_redis_connection
from redis import Redis
from django.core.cache import caches
# from time import time
from datetime import datetime, timezone
class FileServerGenericViewSet(viewsets.GenericViewSet):
    def get_serializer_class(self):
        return FileServerTbSerializer
    def get_queryset(self):
        return 
    
    def create(self,request):
        """
        推送到第三方服务计算
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            file_id = serializer.validated_data['upload_file_tb'].id
            process_server_id = serializer.validated_data['process_server_tb'].id
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
                res = third_response.json()
                # task_cahes = caches['task_cache']
                task_caches: Redis = get_redis_connection('task_cache')

                insert_mapping = {
                    f'{instance_file.filename}:{instance_server.server_content}:{task_id}' : datetime.now(timezone.utc).timestamp()*1000
                }
                task_caches.zadd(
                    'ocr_taskid',
                    insert_mapping,
                    nx=True
                )

                # task_cahes.zadd(
                #     name=f'{file_id}:{process_server_id}',
                #     value=res['task_id']
                # )
                
                return Response({'msg':'success','code':200,'data':[{}]},status=status.HTTP_200_OK)

            except Exception as e:
                return Response(e)
        else:
            Response(serializer.errors)


    def list(self,request):
        """
        列出在redis队列中的全部任务
        """
        task_caches :Redis = get_redis_connection('task_cache')

        value_list = task_caches.zrevrange('ocr_taskid',0,9)
        value_list: list[str] = [ item.decode('utf-8') for item in value_list ]
        res = []
        for item in value_list:
            file_name, server_content, task_id = item.split(':')
            res.append(
                {
                    'file_name':file_name,
                    'server_content':server_content,
                    'task_id':task_id
                }
            )
    
        print(value_list)
        return Response({
            'msg':'看后端',
            'code':200,
            'data':res,
        })

from .serializers import TaskIdSerializer
# 发送前端在状态中的taskid到这个接口上
class TaskStatusGenericAPIView(GenericAPIView):
    def post(self,request):
        serializer = TaskIdSerializer(request.data)
        if serializer.is_valid():
            file_id = serializer.validated_data['taskid']
            "通过file_id，server_id在redis中取出taskid，用taskid 取backend中task的具体任务状态，再序列化成json提供给前端"
            "组合一个key，去redis中查询，xxxbackend_taskid,拿到value,再返回这个查询状态"

        

class TaskDestroyGenericAPIView(GenericAPIView):
    def delete(self,request):
        serializer = FileServerTbSerializer(request.data)
        if serializer.is_valid():
            file_id = serializer.validated_data['upload_file_tb']
            server_id = serializer.validated_data['process_server_tb']
            "通过file_id，server_id在redis中取出taskid，用taskid 取backend中task的具体任务状态，判断状态，队列中可删除，计算中不可删除，已经完成不可删除由系统自动删除"


    





            
            

