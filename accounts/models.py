from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    avatar = models.FileField(upload_to='profiles/', blank=True)
    bio = models.CharField(max_length=160, blank=True)
    location = models.CharField(max_length=80, blank=True)

    def __str__(self):
        return f'{self.user.username} 프로필'

# Create your models here.
