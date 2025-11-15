from django.db import models
from utilis.models import TimeStamp
from django.contrib.auth import get_user_model

User = get_user_model()

class Device(TimeStamp):
    user: User
    attempts: int
    max_attempts: int
    secret_key: str
    last_failed_attempt: "datetime | None"
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_device")
    attempts = models.PositiveSmallIntegerField(default=0)
    max_attempts = models.PositiveSmallIntegerField(default=3)
    secret_key = models.CharField(max_length=16)
    last_failed_attempt = models.DateTimeField(null=True, blank=True)

    def is_valid(self) -> bool:
        """Check if device has not exceeded max attempts"""
        return self.attempts < self.max_attempts

    def reset(self):
        self.attempts = 0
        self.last_failed_attempt = None
        self.save(update_fields=["attempts", "last_failed_attempt"])
        return self
