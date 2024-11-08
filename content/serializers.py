from rest_framework import serializers
from .models import Video, VideoProgress

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'video_file', 'thumbnail', 'category']

class VideoProgressSerializer(serializers.ModelSerializer):
    video = VideoSerializer()
    class Meta:
        model = VideoProgress
        fields = ['video', 'started', 'last_position', 'completed', 'updated_at']