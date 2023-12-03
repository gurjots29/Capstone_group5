

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.shortcuts import redirect

from apps.users.models import Organization, Skill, Volunteer, OrganizationMembership
from .models import Event, RegistrationEvents, Program
from .serializers import EventSerializer, RegistrationEventsSerializer, ProgramSerializer
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required


class EventViewSet(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    # def perform_create(self, serializer):
    #     try:
    #         event = serializer.save()
    #         user = self.request.user
    #         volunteer = Volunteer.objects.get(user=user)
    #         event.organization = volunteer.organization
    #         event.save()
    #     except Exception as e:
    #         print(e)
    #         raise serializers.ValidationError(str(e))



class CreateEventView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            event = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class RegistrationEventsViewSet(generics.ListCreateAPIView):
    queryset = RegistrationEvents.objects.all()
    serializer_class = RegistrationEventsSerializer


class ProgramViewSet(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


@login_required
def events_management_view(request):    
    try:
        volunteer = Volunteer.objects.get(user=request.user)
    except Volunteer.DoesNotExist:
        return render(request, 'no_volunteer_error.html', {'error': 'No se encontró el perfil de Volunteer.'})

    admin_owner_roles = ['admin', 'owner']
    organization_ids = OrganizationMembership.objects.filter(
    volunteer=volunteer, 
    role__in=admin_owner_roles
    ).values_list('organization_id', flat=True)

    organizations = Organization.objects.filter(id__in=organization_ids)


    programs = Program.objects.all()
    skills = Skill.objects.all()
   
   # Filter events belonging to the filtered organizations
    events = Event.objects.filter(organization__id__in=organization_ids)

    return render(request, 'events-management.html', {
        'organizations': organizations,
        'programs': programs,
        'skills': skills,
        'events': events,  # Agregar eventos al contexto
    })





def events_view(request):
    
    if not request.user.is_authenticated:
        return redirect('login')

    volunteer = get_object_or_404(Volunteer, user=request.user)

    admin_owner_roles = ['admin', 'owner']
    organization_ids = OrganizationMembership.objects.filter(
    volunteer=volunteer, 
    role__in=admin_owner_roles
    ).values_list('organization_id', flat=True)

    organizations = Organization.objects.filter(id__in=organization_ids)


    programs = Program.objects.all()
    skills = Skill.objects.all()
   
   # Filter events belonging to the filtered organizations
    events = Event.objects.filter(organization__id__in=organization_ids)

    return render(request, 'view-events.html', {
        'organizations': organizations,
        'programs': programs,
        'skills': skills,
        'events': events,  # Agregar eventos al contexto
    })

def no_volunteer_error(request):
    return render(request, 'no_volunteer_error.html')

    