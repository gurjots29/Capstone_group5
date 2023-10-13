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
    friends = models.ManyToManyField('self')    #namsik
    members = models.ManyToManyField('self')    #namsik

    # def __str__(self):
    #    return f"{self.first_name} {self.last_name}"


class Organization(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='organization_logos/', blank=True)
    friends = models.ManyToManyField('self')    #namsik
    members = models.ManyToManyField('self')    #namsik


    def __str__(self):
        return self.name

#namsik add the model for friendship and membership

class FriendshipRequest(models.Model):
    SENT = 'sent'
    ACCEPTED = 'accepted'

    STATUS_CHOICES = (
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
    )

    created_for = models.ForeignKey(User, related_name='received_friendshiprequests', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='created_friendshiprequests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SENT)


class MembershipRequest(models.Model):
    SENT = 'sent'
    ACCEPTED = 'accepted'

    STATUS_CHOICES = (
        (SENT, 'Sent'),
        (ACCEPTED, 'Accepted'),
    )

    created_for = models.ForeignKey(User, related_name='received_membershiprequests', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='created_membershiprequests', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SENT)
