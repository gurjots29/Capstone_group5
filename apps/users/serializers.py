from rest_framework import serializers
from .models import Badge, Skill, Volunteer, Organization, FriendshipRequest, MembershipRequest


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class VolunteerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Volunteer
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class FriendshipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = '__all__'


class MembershipRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipRequest
        fields = '__all__'