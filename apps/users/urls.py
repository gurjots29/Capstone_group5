from django.urls import path
from .views import BadgeListCreateView, SkillListCreateView, VolunteerListCreateView, OrganizationListCreateView

urlpatterns = [
    path('badges/', BadgeListCreateView.as_view(), name='badge-list-create'),
    path('skills/', SkillListCreateView.as_view(), name='skill-list-create'),
    path('volunteers/', VolunteerListCreateView.as_view(), name='volunteer-list-create'),
    path('organizations/', OrganizationListCreateView.as_view(), name='organization-list-create'),
]
