from django.urls import path, include
from .views import VideoList
from rest_framework.routers import DefaultRouter
from .views import VideoList, VideoProgressViewSet

router = DefaultRouter()
router.register(r'video-progress', VideoProgressViewSet, basename='video-progress')

urlpatterns = [
    path('videos/', VideoList.as_view(), name='video-list'),
    path('', include(router.urls)),
]