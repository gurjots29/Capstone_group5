from django.urls import path
from post.views import PostListCreate, CommentListCreate

urlpatterns = [
    path('postlist/', PostListCreate.as_view(), name='api_posts_list_create'),
    path('comment/', CommentListCreate.as_view(), name='api_comments_list_create'),

]