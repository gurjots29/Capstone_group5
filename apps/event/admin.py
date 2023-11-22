from django.contrib import admin
from .models import Event,RegistrationEvents,Program

admin.site.register(Event)
admin.site.register(RegistrationEvents)
admin.site.register(Program)