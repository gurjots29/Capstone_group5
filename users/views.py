from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.generic.detail import DetailView
from .models import Badge, Skill, Volunteer, Organization, OrganizationMembership, User
from .serializers import BadgeSerializer, SkillSerializer, VolunteerSerializer, OrganizationSerializer
from .forms import LoginForm, SignupForm
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.contrib import messages


class BadgeListCreateView(generics.ListCreateAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer


class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class SkillRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    lookup_field = 'id'


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = Skill.objects.all()  # Añade todas las habilidades al contexto
        return context


class VolunteerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return Response({"error": "Hubo un error al actualizar el voluntario."}, status=status.HTTP_400_BAD_REQUEST)


def profile_volunteers_view(request):
    return render(request, 'profile-volunteer.html')


class AddSkillToVolunteerView(APIView):
    def post(self, request, id, *args, **kwargs):
        volunteer = get_object_or_404(Volunteer, id=id)
        skill_id = request.data.get("skill_id")
        skill = get_object_or_404(Skill, id=skill_id)

        volunteer.skills.add(skill)
        volunteer.save()

        return Response({"message": "Skill added successfully."}, status=status.HTTP_200_OK)


class RemoveSkillFromVolunteerView(APIView):
    def post(self, request, id, *args, **kwargs):
        volunteer = get_object_or_404(Volunteer, id=id)
        skill_id = request.data.get("skill_id")
        skill = get_object_or_404(Skill, id=skill_id)

        if skill in volunteer.skills.all():
            volunteer.skills.remove(skill)
            volunteer.save()
            return Response({"message": "Skill removed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Skill not found in the volunteer's skills."}, status=status.HTTP_400_BAD_REQUEST)


class OrganizationListCreateView(generics.ListCreateAPIView):
    serializer_class = OrganizationSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        memberships = OrganizationMembership.objects.filter(volunteer__user=user)
        return Organization.objects.filter(organizationmembership__in=memberships)

    def perform_create(self, serializer):
        try:
            organization = serializer.save()
            volunteer = self.request.user.volunteer
            OrganizationMembership.objects.create(volunteer=volunteer, organization=organization, role='owner')
        except Exception as e:
            raise serializer.ValidationError(str(e))


class OrganizationDetailView(DetailView):
    model = Organization
    template_name = 'profile-organization.html'
    context_object_name = 'organization'

    def get_object(self, queryset=None):
        org_id = self.kwargs.get('org_id')  # Obtén el ID desde la URL
        return get_object_or_404(Organization, id=org_id)


class OrganizationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    lookup_field = 'id'
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return Response({"error": "Error updating the organization."}, status=status.HTTP_400_BAD_REQUEST)


def my_organizations_view(request):
    return render(request, 'my-organizations.html')


def profile_organizations_view(request):
    return render(request, 'profile-organization.html')


def organization_memberships_view(request):
    return render(request, 'organization-memberships.html')

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
                    return render(request, 'login.html', {'form': form, 'error': 'Account disabled'})
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            # Get form data
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Check if the username is already in use
            if User.objects.filter(username=username).exists():
                messages.error(request, "This username is already taken.")
            # Check if the email address is already in use
            elif User.objects.filter(email=email).exists():
                messages.error(request, "This email address is already registered.")
            else:
                # Create a new user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )

                # Log in the user
                login(request, user)

                # Add a success message
                messages.success(request, "Signup successful!")

                # Redirect to the home page after successful signup
                return redirect('home:home')
    else:
        form = SignupForm()
    return render(request, "sign-up.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect('users:login')

def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {
        "user": user,
    }
    return render(request, "profile-volunteer.html", context)


def followers(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {
        "user": user,
        "title": "Followers",
        "relationships": user.follower_relationships.all(),
    }
    return render(request, "followers.html", context)



def following(request, user_id):
    user = get_object_or_404(User, id=user_id)
    context = {
        "user": user,
        "title": "Following",
        "relationships": user.following_relationships.all(),
    }
    return render(request, "following.html", context)



def follow(request, user_id):
    user = request.user
    target_user = get_object_or_404(User, id=user_id)

    if target_user in user.following.all():
        user.following.remove(target_user)

    else:
        user.following.add(target_user)

    url_next = reverse("users:following", args=[user.id])
    return HttpResponseRedirect(url_next)

def follow1(request, user_id):
    user = request.user
    target_user = get_object_or_404(User, id=user_id)

    if target_user in user.following.all():
        user.following.remove(target_user)

    else:
        user.following.add(target_user)

    url_next = reverse("users:profile", args=[target_user.id])
    return HttpResponseRedirect(url_next)



def organization_memberships_view(request):
    return render(request, 'organization-memberships.html')