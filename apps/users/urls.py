from django.urls import path
from .views import user_logout,user_login,forgot_password_view,profile_organizations_view, profile_volunteers_view, BadgeListCreateView, SkillListCreateView, VolunteerListCreateView, OrganizationListCreateView,VolunteerDetailView

app_name = 'users'

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='user_logout'),
    path('badges/', BadgeListCreateView.as_view(), name='badge-list-create'),
    path('skills/', SkillListCreateView.as_view(), name='skill-list-create'),
    path('volunteers/', VolunteerListCreateView.as_view(), name='volunteer-list-create'),
    path('volunteers/<int:pk>/', VolunteerDetailView.as_view(), name='volunteer-detail'),
    path('organizations/', OrganizationListCreateView.as_view(), name='organization-list-create'),
    path('profile-organizations/', profile_organizations_view, name='profile-organizations'),
    path('profile-volunteer/', profile_volunteers_view, name='profile-volunteer'),
    path('forgot-password/', forgot_password_view, name='forgot-password'),
]
