from django.db import models

# Create your models here.

class PingTb(models.Model):
    ping = models.CharField(max_length=255)


class FileServerTb(models.Model):
    id = models.BigAutoField(primary_key=True)
    upload_file_tb = models.ForeignKey('UploadFileTb', models.DO_NOTHING)
    process_server_tb = models.ForeignKey('ProcessServerTb', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'file_server_tb'


class ProcessServerTb(models.Model):
    id = models.BigAutoField(primary_key=True)
    server_content = models.CharField(max_length=255)
    server_backend = models.CharField(max_length=2048)

    class Meta:
        managed = False
        db_table = 'process_server_tb'


class UploadFileProcessedTb(models.Model):
    id = models.BigAutoField(primary_key=True)
    upload_file_tb = models.ForeignKey('UploadFileTb', models.DO_NOTHING)
    processed_file = models.CharField(max_length=2048)
    processed_file_type = models.CharField(max_length=255)
    create_time = models.DateTimeField(blank=True, null=True)

    # add manytomany
    

    class Meta:
        managed = False
        db_table = 'upload_file_processed_tb'


class UploadFileTb(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.IntegerField()
    filename = models.CharField(max_length=255)
    file = models.FileField(max_length=512,upload_to=r'uploads/%Y-%m-%d/')
    file_type = models.CharField(max_length=255)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'upload_file_tb'

