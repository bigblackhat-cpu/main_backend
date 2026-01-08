from rest_framework import serializers
from .models import FileServerTb, ProcessServerTb, UploadFileProcessedTb, UploadFileTb, PingTb


class PingTbSerializer(serializers.ModelSerializer):
    class Meta:
        model = PingTb
        fields = '__all__'

class UploadFileTbSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    class Meta:
        model = UploadFileTb
        fields = ['file']
class UploadFileTbRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFileTb
        fields = '__all__'
class ListUploadFileTbSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFileTb
        fields = '__all__'

class ListUploadFileProcessedTbSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFileProcessedTb
        fields = '__all__'

class UploadFileProcessedTbSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFileProcessedTb
        fields = ['processed_file','upload_file_tb']

class ProcessServerTbSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessServerTb
        fields = '__all__'





class FileServerTbSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileServerTb
        fields = ['upload_file_tb', 'process_server_tb']

class TaskIdSerializer(serializers.Serializer):
    taskid= serializers.CharField(max_length =1000)
    



