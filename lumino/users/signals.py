# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from .models import Profile

# @receiver(post_save, sender=get_user_model())
# def create_empty_profile(sender, instance, created, using, update_fields, raw=False, **kwargs):
#     if not any(Profile.objects.get(user=instance.pk)):
#         Profile.objects.create(
#             user = instance,
#         )
