from django.db import models
from users.models import Organization, Skill, Volunteer
# Create your models here.
#from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    google_maps_location = models.URLField(max_length=255)
    image = models.ImageField(upload_to='event_images/')
    organization = models.ForeignKey('users.Organization', on_delete=models.CASCADE)
    program = models.ForeignKey('Program', on_delete=models.CASCADE)
    skills_required = models.ForeignKey('users.Skill', on_delete=models.CASCADE)
    max_participants = models.PositiveIntegerField()
    total_hours = models.PositiveIntegerField()
    privacy = models.CharField(
        max_length=15,
        choices=[
            ('public', 'Public'),
            ('private', 'Private'),
            ('invite-only', 'Invite Only'),
        ]
    )

    def _str_(self):  # Corrected string representation method
        return self.title


class RegistrationEvents(models.Model):  # Fixed the indentation
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    volunteer = models.ForeignKey('users.Volunteer', on_delete=models.CASCADE)  # Update with app_name if necessary
    registration_time = models.DateTimeField(auto_now_add=True)
    checkin_time = models.DateTimeField(blank=True, null=True)

    def _str_(self):  
        return self.event.title

        
class Program(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name
