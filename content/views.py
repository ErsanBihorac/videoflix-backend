from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from content.models import Video, VideoProgress
from content.serializers import VideoProgressSerializer, VideoProgressUpdateSerializer, VideoSerializer
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
        """
        Returns list with all videos that have progress of watching
        """
        user = request.user
        in_progress_videos = VideoProgress.objects.filter(user=user, started=True ,completed=False).select_related('video')

        serializer = VideoProgressSerializer(in_progress_videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def save_progress(self, request, pk=None):
        """
        Saves the progress of the target video
        """
        user = request.user
        serializer = VideoProgressUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        video = self._get_video_or_404(pk)
        serializer.save_progress(user=user, video=video)
        return Response({'status': 'Progress saved successfully.'}, status=status.HTTP_200_OK)

    def _get_video_or_404(self, pk):
        """
        Retrieves the Video object or raises a NotFound exception
        """
        try:
            return Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            raise NotFound(detail='Video not found.')