from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from otp.models import Device
from otp.service import OTPService

User = get_user_model()

@receiver(post_save, sender=User)
def create_device(sender, instance, created, **kwargs):
    if created:
        Device.objects.create(user=instance)

@receiver(post_save, sender=User)
def send_otp(): pass