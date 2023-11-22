from .models import Badge, Skill, Volunteer, Organization,OrganizationMembership, Interest, Relationship
from .serializers import BadgeSerializer, SkillSerializer, VolunteerSerializer, OrganizationSerializer
from .forms import LoginForm, SignupForm
from django.urls import reverse
from django.views.generic.detail import DetailView
from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import Http404
from django.http.response import JsonResponse
from django.http import HttpResponseRedirect

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


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
        context['interests'] = Interest.objects.all()  # Añade todas las habilidades al contexto
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


class AddInterestToVolunteerView(APIView):
    def post(self, request, id, *args, **kwargs):
        volunteer = get_object_or_404(Volunteer, id=id)
        interest_id = request.data.get("interest_id")
        interest = get_object_or_404(Interest, id=interest_id)

        volunteer.interests.add(interest)
        volunteer.save()

        return Response({"message": "Interest added successfully."}, status=status.HTTP_200_OK)

class RemoveInterestFromVolunteerView(APIView):
    def post(self, request, id, *args, **kwargs):
        volunteer = get_object_or_404(Volunteer, id=id)
        interest_id = request.data.get("interest_id")
        interest = get_object_or_404(Interest, id=interest_id)

        if interest in volunteer.interests.all():
            volunteer.interests.remove(interest)
            volunteer.save()
            return Response({"message": "Interest removed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Interest not found in the volunteer's interests."}, status=status.HTTP_400_BAD_REQUEST)
        
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
            raise serializers.ValidationError(str(e))


class AddInterestToOrganizationView(APIView):
    def post(self, request, id, *args, **kwargs):
        organization  = get_object_or_404(Organization, id=id)
        interest_id = request.data.get("interest_id")
        interest = get_object_or_404(Interest, id=interest_id)

        organization.interests.add(interest)
        organization.save()

        return Response({"message": "Interest added successfully."}, status=status.HTTP_200_OK)

class RemoveInterestFromOrganizationView(APIView):
    def post(self, request, id, *args, **kwargs):
        organization = get_object_or_404(Organization, id=id)
        interest_id = request.data.get("interest_id")
        interest = get_object_or_404(Interest, id=interest_id)

        if interest in organization.interests.all():
            organization.interests.remove(interest)
            organization.save()
            return Response({"message": "Interest removed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Interest not found in the volunteer's interests."}, status=status.HTTP_400_BAD_REQUEST)
        

class OrganizationDetailView(DetailView):
    model = Organization
    template_name = 'profile-organization.html'
    context_object_name = 'organization'

    def get_object(self, queryset=None):
        org_id = self.kwargs.get('org_id')  # Obtén el ID desde la URL
        return get_object_or_404(Organization, id=org_id)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interests'] = Interest.objects.all()  # Añade todas las habilidades al contexto
        return context
    

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
            # Obtener los datos del formulario
            username = form.cleaned_data["username"]
            first_name = form.cleaned_data["first_name"]  # Cambiar 'name' por 'first_name'
            last_name = form.cleaned_data["last_name"]  # Cambiar 'lastname' por 'last_name'
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Verificar si el nombre de usuario o email ya están en uso
            if User.objects.filter(username=username).exists():
                messages.error(request, "This username is already taken.")

            elif User.objects.filter(email=email).exists():
                messages.error(request, "This email address is already registered.")
            else:
                # Crear un nuevo usuario
                user = User.objects.create_user(
                    username=username, 
                    first_name=first_name,  # Utilizar 'first_name'
                    last_name=last_name,    # Utilizar 'last_name'
                    email=email, 
                    password=password
                )

                # Crear el perfil de Volunteer asociado al usuario
                Volunteer.objects.create(user=user)

                # Iniciar sesión automáticamente con el usuario
                login(request, user)

                # Agregar un mensaje de éxito
                messages.success(request, "Signup successful!")

                # Redirigir a la página de inicio después del registro exitoso
                return redirect('home:home')
    else:
        form = SignupForm()

    return render(request, "sign-up.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect('users:login')



@login_required
@api_view(['POST'])
def update_profile_picture(request, id):
    volunteer = get_object_or_404(Volunteer, id=id)
    profile_picture = request.FILES.get('profile_picture')
    if profile_picture:
        volunteer.profile_picture = profile_picture
        volunteer.save()
        # Obtén la URL de la imagen recién guardada
        new_profile_picture_url = volunteer.profile_picture.url
        # Devuelve esa URL en la respuesta
        return JsonResponse({'newProfilePictureUrl': request.build_absolute_uri(new_profile_picture_url)})
    return Response({'error': 'No profile picture provided.'}, status=400)

@login_required
@api_view(['POST'])
def update_background_image(request, id):
    volunteer = get_object_or_404(Volunteer, id=id)
    background_image = request.FILES.get('background_image')
    if background_image:
        volunteer.background_image = background_image
        volunteer.save()
        # Obtén la URL de la imagen recién guardada
        new_background_image_url = volunteer.background_image.url
        # Devuelve esa URL en la respuesta
        return JsonResponse({'newBackgroundImageUrl': request.build_absolute_uri(new_background_image_url)})
    return Response({'error': 'No background image provided.'}, status=400)



@login_required
@api_view(['POST'])
def update_profile_logo(request, id):
    organization = get_object_or_404(Organization, id=id)
    logo = request.FILES.get('logo')  
    if logo:
        organization.logo = logo  
        organization.save()
        # Obtén la URL de la imagen recién guardada
        new_profile_logo_url = organization.logo.url  
        # Devuelve esa URL en la respuesta
        return JsonResponse({'newProfileLogoUrl': request.build_absolute_uri(new_profile_logo_url)})
    return Response({'error': 'No profile logo provided.'}, status=400)

@login_required
@api_view(['POST'])
def update_obackground_image(request, id):
    organization = get_object_or_404(Organization, id=id)
    obackground_image = request.FILES.get('background_image')
    if obackground_image:
        organization.background_image = obackground_image
        organization.save()
        # Obtén la URL de la imagen recién guardada
        new_obackground_image_url = organization.background_image.url
        # Devuelve esa URL en la respuesta
        return JsonResponse({'newoBackgroundImageUrl': request.build_absolute_uri(new_obackground_image_url)})
    return Response({'error': 'No background image provided.'}, status=400)


def VolunteerRelationships(request):
    try:
        volunteer = request.user.volunteer
    except Volunteer.DoesNotExist:
        return redirect('home')  # Asegúrate de que 'home' sea el nombre de la vista, no el template

    # Obtiene los seguidores del voluntario
    followers = volunteer.follower_relationships.all()

    # Obtiene los voluntarios que el usuario actual está siguiendo
    following = volunteer.following_volunteers.all()

    context = {
        "volunteer": volunteer,
        "title": "Followers and Following",
        "followers": followers,  # Lista de seguidores
        "following": following,  # Lista de voluntarios seguidos
    }
    return render(request, "relationships.html", context)

@login_required
def unfollow_volunteer(request, volunteer_id):
    if request.method == 'POST':
        # Obtener el voluntario a dejar de seguir
        volunteer_to_unfollow = get_object_or_404(Volunteer, id=volunteer_id)

        # Obtener la relación y eliminarla
        Relationship.objects.filter(from_volunteer=request.user.volunteer, to_volunteer=volunteer_to_unfollow).delete()

        # Devolver una respuesta JSON
        return JsonResponse({"success": True})

    return JsonResponse({"success": False})