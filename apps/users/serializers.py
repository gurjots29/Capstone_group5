from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Badge, Skill, Volunteer, Organization
import datetime


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class VolunteerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Volunteer
        fields = ('id', 'phone_number', 'experiences', 'interests', 'location', 'date_of_birth', 'user', 'badges', 'skills')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        badges_data = validated_data.pop('badges', None)
        skills_data = validated_data.pop('skills', None)
        
        # Actualizar los campos de Volunteer
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Aquí puedes manejar cómo deseas actualizar la información del User si es necesario
        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        if badges_data is not None:
            instance.badges.set(badges_data)

        if skills_data is not None:
            instance.skills.set(skills_data)

        instance.save()
        return instance



class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
