from content.tasks import convert_video_for_HLS_player, delete_video_files
from .models import Video
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
import django_rq

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created:    
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(convert_video_for_HLS_player, instance.video_file.path, instance.id, instance.thumbnail.path)

@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.video_file:
        queue = django_rq.get_queue('default', autocommit=True)
        queue.enqueue(delete_video_files, instance.id)
