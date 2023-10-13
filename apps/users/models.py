<<<<<<< HEAD
# myapp/models.py
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    # Add other fields as needed

    def __str__(self):
        return self.title
=======
from django.contrib.auth.models import User
from django.db import models


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
    

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Add a foreign key to the User model
    file = models.FileField(upload_to='post_files/', null=True, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Add a foreign key to the User model

    def __str__(self):
        return self.text
>>>>>>> 5afe1c1 (Pushing for POST API and Comments API)
