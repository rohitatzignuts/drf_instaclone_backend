from django.urls import path
from social.views import (
    PostCreateView,
    PostListView,
    AllPostView,
    PostLikeView,
    CommentCreateView,
)

urlpatterns = [
    path("", PostCreateView.as_view(), name="post-create"),
    path("list", PostListView.as_view(), name="post-list"),
    path("all", AllPostView.as_view(), name="post-full-list"),
    path("<int:post_id>/like/", PostLikeView.as_view(), name="post-like"),
    path(
        "<int:post_id>/comments/",
        CommentCreateView.as_view(),
        name="add-create",
    ),
]
