from django.db import models
from django.contrib.auth.models import User  


class Badge(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='badge_images/')

    def __str__(self):
        return self.name
    
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='volunteer_profile/', blank=True, null=True)
    background_image = models.ImageField(upload_to='volunteer_profile/', blank=True, null=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20)
    experiences = models.TextField()
    interests = models.TextField()
    badges = models.ManyToManyField(Badge, related_name='volunteers', blank=True)
    skills = models.ManyToManyField(Skill, related_name='volunteers', blank=True)
    location = models.CharField(max_length=255, blank=True, null=True)  # Consider using a more detailed location model or a library like django-cities for more granularity
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Organization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='organization_profile/', blank=True)
    background_image = models.ImageField(upload_to='organization_profile/', blank=True, null=True)
    volunteers = models.ManyToManyField(Volunteer, through='OrganizationMembership', related_name='organizations')

    def __str__(self):
        return self.name
    
class OrganizationMembership(models.Model):
    ROLES = (
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('member', 'Member'),
    )
    
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # Asegurando que un Volunteer solo tenga un tipo de rol específico en una organización
            models.UniqueConstraint(
                fields=['volunteer', 'organization', 'role'],
                name='unique_membership'
            )
        ]

class Follower(models.Model):
    follower_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followings")
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, blank=True, null=True, related_name="followers")
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, blank=True, null=True, related_name="followers")
    date_followed = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(volunteer__isnull=False, organization__isnull=True) |
                    models.Q(volunteer__isnull=True, organization__isnull=False)
                ),
                name='only_one_follow_target'
            ),
            models.UniqueConstraint(
                fields=['follower_user', 'volunteer', 'organization'],
                name='unique_follow'
            )
        ]
