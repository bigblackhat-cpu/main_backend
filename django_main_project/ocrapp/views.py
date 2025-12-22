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
