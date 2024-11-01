from django.db import models
from datetime import date

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