# views.py
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users to access this view

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate a token for the new user
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "message": "User created successfully",
                    "token": token.key,
                    "username": user.username,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLogoutView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response(
                {"message": "Logged out successfully"}, status=status.HTTP_200_OK
            )
        except (AttributeError, Token.DoesNotExist):
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class UserDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # The user is available through `request.user` after token authentication
        user = request.user

        # Return user data (you can adjust this based on your needs)
        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        )
