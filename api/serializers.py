from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("author", "title", "body", "creation_date",)


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,)

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(UserSerializer, self).create(validated_data)


class UserInfoSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    last_request = serializers.DateTimeField(read_only=True)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("user", "post", "like", "date",)


class LikeAnalyticsSerializer(serializers.Serializer):
    date = serializers.CharField(max_length=20, read_only=True, source='date__date')
    count = serializers.IntegerField(read_only=True)