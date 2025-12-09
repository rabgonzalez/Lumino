from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = 'S','Student'
        TEACHER = 'T','Teacher'

    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE)
    role = models.CharField(choices=Role, max_length=1, default=Role.STUDENT)
    avatar = models.ImageField(
        blank=True, upload_to='avatars', default='avatars/noavatar.png'
    )
    bio = models.TextField(blank=True)
