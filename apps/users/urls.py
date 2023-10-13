<<<<<<< HEAD
from django.urls import path
from .views import BadgeListCreateView, SkillListCreateView, VolunteerListCreateView, OrganizationListCreateView,VolunteerDetailView

urlpatterns = [
    path('badges/', BadgeListCreateView.as_view(), name='badge-list-create'),
    path('skills/', SkillListCreateView.as_view(), name='skill-list-create'),
    path('volunteers/', VolunteerListCreateView.as_view(), name='volunteer-list-create'),
    path('volunteers/<int:pk>/', VolunteerDetailView.as_view(), name='volunteer-detail'),
    path('organizations/', OrganizationListCreateView.as_view(), name='organization-list-create'),
=======
from django.urls import path
from .views import BadgeListCreateView, SkillListCreateView, VolunteerListCreateView, OrganizationListCreateView,VolunteerDetailView

urlpatterns = [
    path('badges/', BadgeListCreateView.as_view(), name='badge-list-create'),
    path('skills/', SkillListCreateView.as_view(), name='skill-list-create'),
    path('volunteers/', VolunteerListCreateView.as_view(), name='volunteer-list-create'),
    path('volunteers/<int:pk>/', VolunteerDetailView.as_view(), name='volunteer-detail'),
    path('organizations/', OrganizationListCreateView.as_view(), name='organization-list-create'),
]
>>>>>>> 5afe1c1 (Pushing for POST API and Comments API)
