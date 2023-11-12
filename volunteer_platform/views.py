from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from post.models import Post


def home(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-created_at').select_related('user')
        return render(request, 'home.html', {'posts': posts})
    else:
        return redirect('users:login')