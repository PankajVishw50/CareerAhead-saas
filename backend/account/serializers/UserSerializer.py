from rest_framework import serializers
from django.contrib.auth import get_user_model
from util.models.shortcuts import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "image",
            "name",
            "gender",
            "is_superuser",
            "is_active",
            "is_counsellor",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "image",
            "gender",
        ]
