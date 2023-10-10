from django.urls import path
from .views import PostListCreateView, CommentListCreateView

urlpatterns = [
    path('post/', PostListCreateView.as_view(), name='post-list-create'),
    path('comment/', CommentListCreateView.as_view(), name='comment-list-create'),
   
]
