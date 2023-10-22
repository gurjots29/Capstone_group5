

# Create your views here.
from rest_framework import generics
from .models import Event, RegistrationEvents, Program
from .serializers import EventSerializer, RegistrationEventsSerializer, ProgramSerializer

class EventViewSet(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class RegistrationEventsViewSet(generics.ListCreateAPIView):
    queryset = RegistrationEvents.objects.all()
    serializer_class = RegistrationEventsSerializer

class ProgramViewSet(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
