from rest_framework import serializers
from accounts.models import CustomUser
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "profile_pic"]

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.profile_pic.url)
        return None


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    profile_pic = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            "profile_pic",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        ]

    def create(self, validated_data):
        # Extract profile_pic from validated_data
        profile_pic = validated_data.pop("profile_pic", None)

        # Create the user
        user = CustomUser.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        user.set_password(validated_data["password"])

        # Save the profile picture if provided
        if profile_pic:
            user.profile_pic = profile_pic
            user.save()

        return user
