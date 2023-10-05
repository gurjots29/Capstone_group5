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
    phone_number = models.CharField(max_length=20)
    experiences = models.TextField()
    interests = models.TextField()
    badges = models.ManyToManyField(Badge, related_name='volunteers', blank=True)
    skills = models.ManyToManyField(Skill, related_name='volunteers', blank=True)
  

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='organization_logos/', blank=True)


    def __str__(self):
        return self.name