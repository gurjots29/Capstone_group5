from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login,logout
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics
from django.views.generic.detail import DetailView
from .models import Badge, Skill, Volunteer, Organization
from .serializers import BadgeSerializer, SkillSerializer, VolunteerSerializer, OrganizationSerializer
from .forms import LoginForm

class BadgeListCreateView(generics.ListCreateAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class VolunteerListCreateView(generics.ListCreateAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

class VolunteerDetailView(DetailView):
    model = Volunteer
    template_name = 'profile-volunteer.html'
    context_object_name = 'volunteer'

    def get_object(self, queryset=None):
        try:
            return self.request.user.volunteer
        except Volunteer.DoesNotExist:
            raise Http404("No Volunteer associated with this user.")

class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer


def profile_organizations_view(request):
    return render(request, 'profile-organizations.html')

def profile_volunteers_view(request):
    return render(request, 'profile-volunteer.html')


def forgot_password_view(request):
    return render(request, 'forgot-password.html')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home:home')
                else:
                    return render(request, 'login.html', {'form': form, 'error': 'Account disable'})
            else:
                return render(request, 'login.html', {'form': form, 'error': 'invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('users:login')