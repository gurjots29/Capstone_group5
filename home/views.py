from django.shortcuts import render, redirect
from post.models import Post


# from apps.post.models import Post
# Create your views here.

# def home(request):
#    return render(request, 'home.html')

#
def home(request):
        if request.user.is_authenticated:
            posts = Post.objects.all().order_by('-created_at').select_related('user')
            return render(request, 'home.html', {'posts': posts})
        else:
            return redirect('users:login')