from django.contrib import admin
from .models import Video, VideoProgress
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class VideoResource(resources.ModelResource):
    class Meta:
        model = Video

@admin.register(Video)

class VideoAdmin(ImportExportModelAdmin):
    pass

@admin.register(VideoProgress)
class VideoProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'started', 'last_position', 'completed', 'updated_at')
    list_filter = ('completed', 'started')
    search_fields = ('user__username', 'video__title')
    ordering = ('-updated_at',)