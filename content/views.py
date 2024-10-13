from django.shortcuts import render
from rest_framework import generics
from content.models import Video
from content.serializers import VideoSerializer

class VideoList(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer