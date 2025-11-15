from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    model = User
    fields = ['email','password','confirm_password']
    extra_kwargs = {
        'password': {'write_only': True}
    }


    def validate(self, attrs):
        pass1 = attrs.get("password")
        pass2 = attrs.get("confirm_password")
        if pass1 != pass2:
            raise serializers.ValidationError("Password Mismatch")
        return attrs
