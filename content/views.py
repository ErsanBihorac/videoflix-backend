from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from content.models import Video, VideoProgress
from content.serializers import VideoProgressSerializer, VideoSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
class VideoList(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

class VideoProgressViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def in_progress(self, request):
        user = request.user
        in_progress_videos = VideoProgress.objects.filter(user=user, started=True ,completed=False).select_related('video')

        serializer = VideoProgressSerializer(in_progress_videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def save_progress(self, request, pk=None):
        user = request.user
        last_position = request.data.get('last_position')

        if last_position is None:
            return Response({'error': 'Last position is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            raise NotFound(detail='Video not found.')
        
        video_progress, created = VideoProgress.objects.get_or_create(
            user=user,
            video=video,
            defaults={'last_position': last_position, 'started': True}
        )

        if not created:
            video_progress.last_position = last_position
            video_progress.save()

        return Response({'status': 'Progress saved successfully.'}, status=status.HTTP_200_OK)