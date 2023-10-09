from rest_framework import generics
from .models import Badge, Skill, Volunteer, Organization
from .serializers import BadgeSerializer, SkillSerializer, VolunteerSerializer, OrganizationSerializer

class BadgeListCreateView(generics.ListCreateAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer

class SkillListCreateView(generics.ListCreateAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class VolunteerListCreateView(generics.ListCreateAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer

class VolunteerDetailView(generics.RetrieveAPIView):
    queryset = Volunteer.objects.all()
    serializer_class = VolunteerSerializer


class OrganizationListCreateView(generics.ListCreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
