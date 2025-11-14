from datetime import  timedelta
from django.db.models import F
import pyotp
from django.utils import timezone

from.models import Device

class OTPService:
    OTP_INTERVAL = 60
    BLOCK_TIME = 300
    MAX_ATTEMPTS = 3

    @staticmethod
    def generate_secret_key() -> str:
        """Generate a new 16-character base32 secret key"""
        return pyotp.random_base32()

    @staticmethod
    def generate_totp(device: Device) -> str:
        """Return current OTP for a device"""
        return pyotp.TOTP(device.secret_key, interval=OTPService.OTP_INTERVAL).now()

    @staticmethod
    def verify_otp(device: Device, otp) -> bool:
        """Verify OTP, handle attempts, cooldown, and secret rotation"""
        # Check if device is blocked
        if device.attempts >= device.max_attempts:
            if device.last_failed_attempt:
                block_until = device.last_failed_attempt + timedelta(seconds=OTPService.BLOCK_TIME)
                if timezone.now() < block_until:
                    return False
                else:
                    device.attempts = 0
                    device.save(update_fields=['attempts'])

        totp = pyotp.TOTP(device.secret_key, interval=OTPService.OTP_INTERVAL)

        if totp.verify(otp):
            # success: reset attempts, rotate secret
            device.secret_key = OTPService.generate_secret_key()
            device.attempts = 0
            device.last_failed_attempt = None
            device.save(update_fields=['secret_key', 'attempts', 'last_failed_attempt'])
            return True
        else:
            # failure: increment attempts atomically
            device.attempts = F('attempts') + 1
            device.last_failed_attempt = timezone.now()
            device.save(update_fields=['attempts', 'last_failed_attempt'])
            return False
