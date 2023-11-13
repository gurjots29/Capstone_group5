from django.contrib import admin
from .models import Interest, Volunteer, Badge, Skill, Organization, Relationship, OrganizationMembership, Category

admin.site.register(Volunteer)
admin.site.register(Badge)
admin.site.register(Skill)
admin.site.register(Organization)
admin.site.register(Relationship)
admin.site.register(OrganizationMembership)
admin.site.register(Category)
admin.site.register(Interest)
