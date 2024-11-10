from django.core.files.uploadedfile import SimpleUploadedFile
from login.models import CustomUser
from .models import Video, VideoProgress

def create_video_file():
    """
    Simulates a video file for testing
    """
    video_file = SimpleUploadedFile(
        name='test_video.mp4',
        content=b'This is a test video Content',
        content_type='video/mp4',
    )

    return video_file

def create_thumbnail():
    """
    Simulates a thumbnail for testing
    """
    thumbnail = SimpleUploadedFile(
        name='test_thumbnail.jpg',
        content=b'',
        content_type='image/jpeg',
    )

    return thumbnail

def create_video():
    """
    Creates a video object for testing
    """
    video_file = create_video_file()
    thumbnail = create_thumbnail()

    video = Video.objects.create(
        title='Video Testing',
        description='This is a unit test.',
        video_file=video_file,
        thumbnail=thumbnail,
        category='documentary'
    )

    return video

def create_custom_user():
    """
    Creates a custom user for testing
    """
    user = CustomUser.objects.create(email='test@mail.com')
    user.set_password('testing_password')
    user.save()

    return user

def create_video_progress(user, video):
    """
    Creates a video progress object for testing
    """
    video_progress = VideoProgress.objects.create(
        user=user,
        video=video,
        started=False,
        last_position=0,
        completed=False
    )

    return video_progress