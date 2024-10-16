from django.contrib.auth import get_user_model
from rest_framework import serializers
from social.models import Post, Comment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "profile_pic"]


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "content", "created_at", "post", "user"]


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ["id", "image", "caption", "created_at", "likes", "user", "comments"]
        read_only_fields = ["user", "created_at"]
