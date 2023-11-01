from django.contrib import admin
from .models import Volunteer, Badge, Skill, Organization, Follower, OrganizationMembership

admin.site.register(Volunteer)
admin.site.register(Badge)
admin.site.register(Skill)
admin.site.register(Organization)
admin.site.register(Follower)
admin.site.register(OrganizationMembership)
