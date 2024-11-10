from django.test import TestCase, Client
from content.utils import create_custom_user, create_video, create_video_progress
from login.models import CustomUser
from .models import Video, VideoProgress
from django.urls import reverse
class TestModels(TestCase):
    def setUp(self):
        self.video = create_video()
        self.user = create_custom_user()
        self.video_progress = create_video_progress(self.user, self.video)

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

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.video = create_video()
        self.user = create_custom_user()
        self.video_progress = create_video_progress(self.user, self.video)
        self.video_list_url = reverse('video-list')
        self.video_progress_in_progress_url = reverse('video-progress-in-progress')
        self.video_progress_save_progress_url = reverse('video-progress-save-progress', args=[self.video_progress.pk])

    def test_video_list_GET_authenticated(self):
        login = self.client.login(username='test@mail.com', password='testing_password')
        response_authenticated = self.client.get(self.video_list_url)
        self.assertTrue(CustomUser.objects.filter(email='test@mail.com').exists())
        self.assertTrue(login)
        self.assertEqual(response_authenticated.status_code, 200)

    def test_video_list_GET_unauthenticated(self):
        response_unauthenticated = self.client.get(self.video_list_url)
        self.assertEqual(response_unauthenticated.status_code, 401)

    def test_video_progress_in_progress_authenticated(self):
        login = self.client.login(username='test@mail.com', password='testing_password')
        response_authenticated = self.client.get(self.video_progress_in_progress_url)
        self.assertTrue(CustomUser.objects.filter(email='test@mail.com').exists())
        self.assertTrue(login)
        self.assertEqual(response_authenticated.status_code, 200)

    def test_video_progress_in_progress_unauthenticated(self):
        response_unauthenticated = self.client.get(self.video_progress_in_progress_url)
        self.assertEqual(response_unauthenticated.status_code, 401)

    def test_video_progress_save_progress_authenticated(self):
        login = self.client.login(username='test@mail.com', password='testing_password')
        response_authenticated = self.client.post(self.video_progress_save_progress_url, data={'last_position': 75})
        self.assertTrue(login)
        self.assertEqual(response_authenticated.status_code, 200)

    def test_video_progress_save_progress_unauthenticated(self):
        response_unauthenticated = self.client.post(self.video_progress_save_progress_url, data={'last_position': 75})
        self.assertEqual(response_unauthenticated.status_code, 401)