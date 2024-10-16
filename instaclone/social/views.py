from django.shortcuts import render
from rest_framework.views import APIView
from social.serializers import PostSerializer, CommentSerializer
from social.models import Post, Comment
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status, generics


# Create your views here.
class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter posts by the authenticated user."""
        return Post.objects.filter(user=self.request.user).order_by("-created_at")


class AllPostView(generics.ListAPIView):
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Show all the posts."""
        return Post.objects.all().order_by("-created_at")


class PostCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        image = request.FILES.get("image")
        caption = request.data.get("caption")

        if image:
            post = Post.objects.create(user=user, image=image, caption=caption)
            return Response(
                {"message": "Post created successfully!"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": "Image is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class PostLikeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            return Response({"message": "Post unliked!"}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({"message": "Post liked!"}, status=status.HTTP_200_OK)


class CommentCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
            user = request.user
            content = request.data.get("content")

            if not content:
                return Response(
                    {"error": "Content is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            comment = Comment.objects.create(post=post, user=user, content=content)
            serializer = CommentSerializer(comment)

            # Combine the message and serialized data in one response
            return Response(
                {"message": "Comment Added.", "comment": serializer.data},
                status=status.HTTP_201_CREATED,
            )

        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND
            )
