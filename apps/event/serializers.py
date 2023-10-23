from rest_framework import serializers
from .models import Event, RegistrationEvents, Program

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class RegistrationEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistrationEvents
        fields = '__all__'

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'
