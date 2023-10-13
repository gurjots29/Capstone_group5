<<<<<<< HEAD
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm


def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'login.html', {'form': form, 'error': 'Cuenta desactivada'})
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Credenciales inválidas'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

=======
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from apps.users.models import Post
from .forms import CommentForm, LoginForm, PostForm, SignupForm
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib import messages

def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            # Get form data
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            
            if User.objects.filter(username=username).exists():
                messages.error(request, "This username is already taken.")
            
            elif User.objects.filter(email=email).exists():
                messages.error(request, "This email address is already registered.")
            else:
                
                user = User.objects.create_user(
                    username=username, email=email, password=password
                )

                
                login(request, user)

                
                messages.success(request, "Signup successful!")

                
                return redirect("user_feed")
    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("user_feed")
                else:
                    return render(
                        request,
                        "login.html",
                        {"form": form, "error": "Cuenta desactivada"},
                    )
            else:
                return render(
                    request,
                    "login.html",
                    {"form": form, "error": "Credenciales inválidas"},
                )
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")


@login_required(login_url='login')
def home(request):
    return render(request, "home.html")


@login_required(login_url='login')
def user_feed(request):
    posts = Post.objects.all().select_related('user')
    return render(request, 'user_feed.html', {'posts': posts})

@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assign the current user to the post
            post.save()
            return redirect('user_feed')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

@login_required(login_url='login')
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # Assign the current user to the comment
            comment.post = post
            comment.save()
            return redirect('user_feed')
    else:
        form = CommentForm()
    return render(request, 'add_comment.html', {'form': form, 'post': post})
>>>>>>> 5afe1c1 (Pushing for POST API and Comments API)
