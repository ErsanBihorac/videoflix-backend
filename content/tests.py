from django.test import TestCase, Client
from content.utils import create_video, create_video_progress
from .models import Video, VideoProgress
class TestModels(TestCase):
    def setUp(self):
        self.video = create_video()
        self.video_progress = create_video_progress()

    def test_model_video(self):
        self.assertEqual(str(self.video), 'Video Testing')
        self.assertTrue(isinstance(self.video, Video))
        self.assertEqual(self.video.description, 'This is a unit test.')
        self.assertEqual(self.video.category, 'documentary')
        self.assertTrue(self.video.video_file)
        self.assertTrue(self.video.thumbnail)

    def test_model_video_progress(self):
        self.assertTrue(isinstance(self.video_progress, VideoProgress))
        self.assertEqual(f"{self.video_progress.user} - {self.video_progress.video.title} - {self.video_progress.last_position}", 'test@mail.com - Video Testing - 0')
        self.assertTrue(self.video_progress.user)
        self.assertTrue(self.video_progress.video)