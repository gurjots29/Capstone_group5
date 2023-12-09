

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.views import APIView
from django.views import View
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.shortcuts import redirect
from django.http import JsonResponse

from apps.users.models import Organization, Skill, Volunteer, OrganizationMembership
from .models import Event, RegistrationEvents, Program
from .serializers import EventSerializer, RegistrationEventsSerializer, ProgramSerializer
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework.permissions import IsAuthenticated

class EventRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventRegisterView(View):
    def post(self, request, event_id, *args, **kwargs):
        event = get_object_or_404(Event, id=event_id)
        user = request.user  # Assuming the user is authenticated


        event.register_users.add(user)

        return JsonResponse({'message': 'Successfully registered for the event'})

class EventUnregisterView(View):
    def post(self, request, event_id, *args, **kwargs):
        print('Hello',event_id)
        event = Event.objects.get(pk = event_id)
        print(event)
        event = get_object_or_404(Event, id=event_id)
        user = request.user  # Assuming the user is authenticated

        event.register_users.remove(user)

        return JsonResponse({'message': 'Successfully unregistered from the event'})

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



def events_management_view(request):
    
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

    return render(request, 'events-management.html', {
        'organizations': organizations,
        'programs': programs,
        'skills': skills,
        'events': events,  # Agregar eventos al contexto
    })





def events_view(request):
    
    if not request.user.is_authenticated:
        return redirect('login')

    #volunteer = get_object_or_404(Volunteer, user=request.user)
    volunteer = Volunteer.objects.first()

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
    
    print('events',events)

    return render(request, 'view-events.html', {
        'organizations': organizations,
        'programs': programs,
        'skills': skills,
        'events': events,  # Agregar eventos al contexto
    })