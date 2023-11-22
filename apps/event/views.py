

# Create your views here.
from rest_framework import generics
from django.shortcuts import render

from apps.users.models import Organization, Skill, Volunteer
from .models import Event, RegistrationEvents, Program
from .serializers import EventSerializer, RegistrationEventsSerializer, ProgramSerializer
from rest_framework import serializers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
from rest_framework.permissions import IsAuthenticated

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


class RegistrationEventsViewSet(generics.ListCreateAPIView):
    queryset = RegistrationEvents.objects.all()
    serializer_class = RegistrationEventsSerializer


class ProgramViewSet(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


def events_management_view(request):
    event_fields = [field.name for field in Event._meta.get_fields()]
    
    # Query related models
    organizations = Organization.objects.all()
    programs = Program.objects.all()
    skills = Skill.objects.all()

    return render(request, 'events-management.html', {
        'event_fields': event_fields,
        'organizations': organizations,
        'programs': programs,
        'skills': skills,
    })