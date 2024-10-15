from django.urls import path
from social.views import PostCreateView, PostListView, AllPostView

urlpatterns = [
    path("", PostCreateView.as_view(), name="post-create"),
    path("list", PostListView.as_view(), name="post-list"),
    path("all", AllPostView.as_view(), name="post-full-list"),
]
