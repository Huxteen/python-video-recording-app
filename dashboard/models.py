from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


class VideoRecord(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    admin_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='admins', default=None, blank=True, null=True)
    video_name = models.ImageField(upload_to='recorded_video/', null=True, blank=True)
    status = models.BooleanField(default=False)   
    updated_at = models.DateTimeField(default=datetime.now, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True, null=True)

    def __int__(self):
        return self.user_id


