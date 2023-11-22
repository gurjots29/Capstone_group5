from django.shortcuts import render
from apps.post.models import Post 
# Create your views here.

#def home(request):
 #   return render(request, 'home.html')


def home(request):
    posts = Post.objects.all().order_by('-created_at').select_related('user')
   #  posts = Post.objects.all().select_related('user')
    return render(request, 'home.html', {'posts': posts})