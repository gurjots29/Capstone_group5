from .models import Category,Badge, Skill, Volunteer, Organization,OrganizationMembership, Interest, Relationship
from .serializers import OrganizationMembershipSerializer, InterestSerializer, BadgeSerializer, SkillSerializer, \
    VolunteerSerializer, OrganizationSerializer, SuggestionSerializer
from .forms import LoginForm, SignupForm

from django.urls import reverse
from django.views.generic.detail import DetailView
from django.views import View

from django.core.exceptions import ObjectDoesNotExist

from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import Http404
from django.http import JsonResponse
from django.http import HttpResponseRedirect

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import NotFound
from django.views.decorators.http import require_POST

from .utils import apply_one_hot_encoding, calculate_match,get_coordinates, calculate_match,calculate_distance
from django.utils.decorators import method_decorator
import json
from ..post.models import Post


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
        id = self.kwargs.get('pk')  # Obtén el ID desde la URL
        return get_object_or_404(Volunteer, id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        volunteer = self.get_object()

        # Añade las habilidades e intereses al contexto
        context['skills'] = Skill.objects.all()  
        context['interests'] = Interest.objects.all()

        # Añade solo las habilidades e intereses del voluntario en cuestión al contexto
        context['volunteer_skills'] = volunteer.skills.all()
        context['volunteer_interests'] = volunteer.interests.all()

        # Obtiene los seguidores y los seguidos del voluntario
        context['followers'] = volunteer.follower_relationships.all() 
        context['following'] = volunteer.following_volunteers.all() 
        context['followed_organizations'] = volunteer.following_organizations.all()

         # Obtiene las organizaciones donde el voluntario es miembro
        member_organizations = OrganizationMembership.objects.filter(
            volunteer=volunteer,
            status='accepted'  # Asume que 'accepted' es un estado de membresía válido
        ).select_related('organization')

        context['member_organizations'] = [membership.organization for membership in member_organizations]


        # Añadir la lógica para verificar si el usuario actual ya sigue al voluntario
        user_is_follower = False
        if self.request.user.is_authenticated and not self.request.user == volunteer.user:
            user_is_follower = Relationship.objects.filter(
                from_volunteer=self.request.user.volunteer,
                to_volunteer=volunteer
            ).exists()

        context['user_is_follower'] = user_is_follower
        return context

class VolunteerDetailView2(DetailView):
    model = Volunteer
    template_name = 'profile-volunteer.html'
    context_object_name = 'volunteer'

    def get_object(self, queryset=None):
        user_id = self.kwargs.get('user_id')
        try:
            volunteer = Volunteer.objects.get(user_id=user_id)
            return volunteer
        except Volunteer.DoesNotExist:
            raise Http404("No Volunteer associated with this user.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skills'] = Skill.objects.all()  # Añade todas las habilidades al contexto
        context['interests'] = Interest.objects.all()  # Añade todas las habilidades al contexto
        context['following'] = self.request.user.volunteer.following_volunteers.all()
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

        # Generar la codificación one-hot
        interests = [i.name for i in volunteer.interests.all()]
        encoded_data = Volunteer.apply_one_hot_encoding(interests)
        volunteer.encoded_data = encoded_data
  
        volunteer.save()

        return Response({"message": "Interest added successfully."}, status=status.HTTP_200_OK)

class RemoveInterestFromVolunteerView(APIView):
    def post(self, request, id, *args, **kwargs):
        volunteer = get_object_or_404(Volunteer, id=id)
        interest_id = request.data.get("interest_id")
        interest = get_object_or_404(Interest, id=interest_id)

        if interest in volunteer.interests.all():
            volunteer.interests.remove(interest)

            # Recalcular la codificación one-hot después de eliminar el interés
            interests = [i.name for i in volunteer.interests.all()]
            encoded_data = Volunteer.apply_one_hot_encoding(interests)
            volunteer.encoded_data = encoded_data

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
            raise serializer.ValidationError(str(e))


class AddInterestToOrganizationView(APIView):
    def post(self, request, id, *args, **kwargs):
        organization  = get_object_or_404(Organization, id=id)
        interest_id = request.data.get("interest_id")
        interest = get_object_or_404(Interest, id=interest_id)

        organization.interests.add(interest)

         # Recalcular la codificación one-hot
        interests = [i.name for i in organization.interests.all()]
        encoded_data = Organization.apply_one_hot_encoding(interests)
        organization.encoded_interests_skills = encoded_data

        organization.save()

        return Response({"message": "Interest added successfully."}, status=status.HTTP_200_OK)

class RemoveInterestFromOrganizationView(APIView):
    def post(self, request, id, *args, **kwargs):
        organization = get_object_or_404(Organization, id=id)
        interest_id = request.data.get("interest_id")
        interest = get_object_or_404(Interest, id=interest_id)

        if interest in organization.interests.all():
            organization.interests.remove(interest)

             # Recalcular la codificación one-hot
            interests = [i.name for i in organization.interests.all()]
            encoded_data = Organization.apply_one_hot_encoding(interests)
            organization.encoded_interests_skills = encoded_data

            organization.save()
            return Response({"message": "Interest removed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Interest not found in the volunteer's interests."}, status=status.HTTP_400_BAD_REQUEST)
        

class OrganizationDetailView(DetailView):
    model = Organization
    template_name = 'profile-organization.html'
    context_object_name = 'organization'

    def get_object(self, queryset=None):
        org_id = self.kwargs.get('pk')  # Obtén el ID desde la URL
        return get_object_or_404(Organization, id=org_id)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organization = self.get_object()
        context['interests'] = Interest.objects.all()

        # Añade los seguidores de la organización al contexto
        context['followers'] = Relationship.objects.filter(to_organization=organization)

        # Lógica para verificar si el usuario actual es 'owner' o 'admin'
        user_is_admin_or_owner = False
        if self.request.user.is_authenticated:
            membership = OrganizationMembership.objects.filter(
                volunteer=self.request.user.volunteer,
                organization=organization,
                role__in=['owner', 'admin']
            ).first()
            if membership:
                user_is_admin_or_owner = True
        
        context['user_is_admin_or_owner'] = user_is_admin_or_owner

         # Añadir la lógica para verificar si el usuario actual ya sigue a la organización
        user_is_follower = False
        if self.request.user.is_authenticated:
            user_is_follower = Relationship.objects.filter(
                from_volunteer=self.request.user.volunteer,
                to_organization=organization
            ).exists()

        context['user_is_follower'] = user_is_follower

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
    if request.user.is_authenticated:
        volunteer = request.user.volunteer
        memberships = OrganizationMembership.objects.filter(volunteer=volunteer, role__in=['owner', 'admin'])
        organizations = [membership.organization for membership in memberships]

        # Asignar la lista de intereses a cada organización
        for org in organizations:
            org.interests_list = ", ".join([interest.name for interest in org.interests.all()])

        context = {
            'organizations': organizations,
        }
    else:
        context = {}

    return render(request, 'my-organizations.html', context)

def profile_organizations_view(request):
    return render(request, 'profile-organization.html')


def organization_memberships_view(request):
    current_volunteer = request.user.volunteer

    user_organizations = Organization.objects.filter(
        organizationmembership__volunteer=current_volunteer,
        organizationmembership__role__in=['owner', 'admin']
    )

    # Aquí agregamos la lógica de ordenación elegida
    memberships = OrganizationMembership.objects.filter(
        organization__in=user_organizations
    ).order_by('status', 'date_joined')  # Ejemplo de ordenación combinada

    volunteers = Volunteer.objects.all()

    context = {
        'memberships': memberships,
        'volunteers': volunteers,  
        'organizations': user_organizations
    }

    return render(request, 'organization-memberships.html', context)

@login_required
@require_POST
def accept_membership_view(request, membership_id):
    membership = get_object_or_404(OrganizationMembership, id=membership_id)

    # Asegúrate de que el usuario actual tiene permiso para aceptar la membresía
    if request.user.volunteer in membership.organization.volunteers.all():
        membership.status = 'accepted'
        membership.save()
        return JsonResponse({'message': 'Membership accepted successfully'})
    else:
        return JsonResponse({'message': 'Unauthorized'}, status=403)
    

def forgot_password_view(request):
    return render(request, 'forgot-password.html')

def get_match_level(match_score):
    # Ajusta estos valores según el nuevo sistema de puntuación
    if match_score >= 10:  # Asumiendo que 10 es un buen puntaje alto
        return 'Strong'
    elif 5 <= match_score < 10:
        return 'Moderate'
    elif match_score < 5:
        return 'Weak'
 
MATCH_THRESHOLD = 2
MATCH_LEVEL_VALUES = {
    'Strong': 3,
    'Moderate': 2,
    'Weak': 1
}
@method_decorator(login_required, name='dispatch')
class VolunteerMatchView(View):
    def get(self, request, *args, **kwargs):
        volunteer = request.user.volunteer

        matches = []
        volunteer_encoded_interests = volunteer.encoded_data
        volunteer_location = volunteer.location
        volunteer_coords = get_coordinates(volunteer_location) if volunteer_location else None

        for organization in Organization.objects.all():
            organization_encoded_interests = organization.encoded_interests_skills
            organization_location = organization.location
            organization_coords = get_coordinates(organization_location) if organization_location else None

            if volunteer_coords and organization_coords:
                distance = calculate_distance(volunteer_coords, organization_coords)
                match_score = calculate_match(volunteer_encoded_interests, organization_encoded_interests, volunteer_coords, organization_coords)
                if match_score >= MATCH_THRESHOLD:
                    membership = OrganizationMembership.objects.filter(volunteer=volunteer, organization=organization).first()

                    if membership:
                        match_status = membership.status
                        is_subscribed = membership.status == 'accepted'
                        is_owner = membership.role == 'owner' and is_subscribed
                        is_admin = membership.role == 'admin' and is_subscribed
                    else:
                        match_status = 'not_member'
                        is_subscribed = False
                        is_owner = False
                        is_admin = False

                    match_level = get_match_level(match_score)
                    organization_interests = ', '.join([interest.name for interest in organization.interests.all()])

                    matches.append({
                        'organization': organization,
                        'distance': distance,
                        'is_subscribed': is_subscribed,
                        'is_owner': is_owner,
                        'is_admin': is_admin,
                        'match_level': match_level,
                        'interests': organization_interests,
                        'match_status': match_status  # Añadir el estado de la membresía
                    })

        matches.sort(key=lambda x: (-MATCH_LEVEL_VALUES.get(x['match_level'], 0), x['distance']))

     
        context = {
            'volunteer': volunteer,
            'matches': matches,
        }
        return render(request, 'organization-match.html', context)
    
    
    def post(self, request, organization_id, *args, **kwargs):
        organization = get_object_or_404(Organization, id=organization_id)
        volunteer = request.user.volunteer

        membership = OrganizationMembership.objects.filter(volunteer=volunteer, organization=organization).first()
        if membership:
            return JsonResponse({"message": "Subscribed"}, status=200)

        OrganizationMembership.objects.create(volunteer=volunteer, organization=organization, role='member')

        return JsonResponse({"message": "Subscribed successfully"}, status=200)

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

    # Obtiene las organizaciones que el voluntario está siguiendo
    followed_organizations = volunteer.following_organizations.all()

    context = {
        "volunteer": volunteer,
        "title": "Followers, Following, and Organizations",
        "followers": followers,  # Lista de seguidores
        "following": following,  # Lista de voluntarios seguidos
        "followed_organizations": followed_organizations,  # Lista de organizaciones seguidas
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

@login_required
def follow_volunteer(request, volunteer_id):
    if request.method == 'POST':
        # Obtener el voluntario a seguir
        volunteer_to_follow = get_object_or_404(Volunteer, id=volunteer_id)

        # Crear la relación de seguimiento (si no existe)
        Relationship.objects.get_or_create(
            from_volunteer=request.user.volunteer, 
            to_volunteer=volunteer_to_follow
        )

        # Devolver una respuesta JSON
        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


class SuggestedVolunteerList(generics.ListAPIView):
    serializer_class = SuggestionSerializer

    def get_queryset(self):
        current_user = self.request.user.volunteer
        following_users = [volunteer.user for volunteer in current_user.following_volunteers.all()]
        return (Volunteer.objects.filter(interests__in=current_user.interests.all(), skills__in=current_user.skills.all())
                .exclude(user=current_user.user)
                .exclude(user__in=following_users)
                .distinct())


@login_required
def unfollow_organization(request, organization_id):
    if request.method == 'POST':
        # Obtener el voluntario a dejar de seguir
        organization_to_unfollow = get_object_or_404(Organization, id=organization_id)

        # Obtener la relación y eliminarla
        Relationship.objects.filter(from_volunteer=request.user.volunteer, to_organization=organization_to_unfollow).delete()

        # Devolver una respuesta JSON
        return JsonResponse({"success": True})

    return JsonResponse({"success": False})

@login_required
def follow_organization(request, organization_id):
    if request.method == 'POST':
        # Obtener el voluntario a seguir
        organization_to_follow = get_object_or_404(Organization, id=organization_id)

        # Crear la relación de seguimiento (si no existe)
        Relationship.objects.get_or_create(
            from_volunteer=request.user.volunteer, 
            to_organization=organization_to_follow 
        )

        # Devolver una respuesta JSON
        return JsonResponse({"success": True})

    return JsonResponse({"success": False})


def skills_admin_view(request):
    skills = Skill.objects.all()  # Obtiene todas las habilidades
    categories = Category.objects.all()  # Obtiene todas las categorías

    context = {
        'skills': skills,
        'categories': categories
    }
    
    return render(request, 'skills-admin.html', context)


class AddSkillView(APIView):
    def post(self, request, *args, **kwargs):
        # Obtener los datos del formulario
        skill_data = request.data

        # Validar y guardar el nuevo Skill
        serializer = SkillSerializer(data=skill_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Skill added successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_BAD_REQUEST)


def interest_admin_view(request):
    interests = Interest.objects.all()  # Obtiene todos los intereses
    categories = Category.objects.filter(category_type='interest')  # Obtiene las categorías de tipo 'interés'

    context = {
        'interests': interests,
        'categories': categories
    }
    
    return render(request, 'interest-admin.html', context)


class AddInterestView(APIView):
    def post(self, request, *args, **kwargs):
        # Obtener los datos del formulario
        interest_data = request.data

        # Validar y guardar el nuevo Interest
        serializer = InterestSerializer(data=interest_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Interest added successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AddOrganizationMembershipView(APIView):
    def post(self, request, *args, **kwargs):
        membership_data = request.data

        serializer = OrganizationMembershipSerializer(data=membership_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Membership added successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@login_required
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        volunteer = get_object_or_404(Volunteer, user=request.user)

        if post in volunteer.like_post.all():
            volunteer.like_post.remove(post)
            return JsonResponse({"success": True, "message": "Post unliked."})

        volunteer.like_post.add(post)
        return JsonResponse({"success": True, "message": "Post liked."})

    return JsonResponse({"success": False, "message": "Invalid HTTP method"})


@login_required
def is_liked(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=post_id)
        volunteer = get_object_or_404(Volunteer, user=request.user)
        if volunteer in post.like_users.all():
            return JsonResponse({"success": True})
    return JsonResponse({"success": False, "message": "Invalid HTTP method"})



