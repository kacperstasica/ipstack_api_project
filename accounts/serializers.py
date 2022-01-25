from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from accounts.models import User
from accounts.validators import drf_based_password_validation


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ("id", "email", "password", "confirm_password")

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        if errors := drf_based_password_validation(validated_data['password']):
            raise ValidationError({'password': errors})
        # for the presentation aspects of this application,
        # we allow registration only for super users
        return User.objects.create_superuser(**validated_data)

    def validate_password(self, password):
        if self.initial_data.get('confirm_password') != password:
            raise serializers.ValidationError('Passwords must match.')
        return password
