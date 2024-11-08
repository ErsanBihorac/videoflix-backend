from django.db import models
from datetime import date
from login.models import CustomUser

class Video(models.Model):
    categories = [
        ('new', 'New on Videoflix'),
        ('documentary', 'Documentary'),
        ('drama', 'Drama'),
        ('romance', 'Romance')
    ]
        
    created_at = models.DateField(default=date.today)
    title = models.CharField(max_length=16)
    description = models.CharField(max_length=256)
    video_file = models.FileField(upload_to='videos', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails', blank=False, null=False)
    category = models.CharField(max_length=16, choices=categories, default='new')

    def __str__(self):
        return self.title
    
class VideoProgress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    started = models.BooleanField(default=False)
    last_position = models.FloatField()
    completed = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.video.title} - {self.last_position}"