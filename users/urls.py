from django.urls import path

from users.views import (
    user_login,
    user_logout,
    user_signup,
    forgot_password_view,
    profile,
    followers,
    following,
    follow, organization_memberships_view, follow1, BadgeListCreateView, SkillListCreateView,
    SkillRetrieveUpdateDestroyView, VolunteerListCreateView, VolunteerDetailView, VolunteerRetrieveUpdateDestroyView,
    AddSkillToVolunteerView, RemoveSkillFromVolunteerView, my_organizations_view, OrganizationListCreateView,
    OrganizationDetailView, OrganizationRetrieveUpdateDestroyView,
)

app_name = 'users'

urlpatterns = [
    # Users
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='user_logout'),
    path('badges/', BadgeListCreateView.as_view(), name='badge-list-create'),
    path('forgot-password/', forgot_password_view, name='forgot-password'),
    path('sign-up/', user_signup, name='sign-up'),
    path("profile/<int:user_id>/", profile, name="profile"),
    path("followers/<int:user_id>/", followers, name="followers"),
    path("following/<int:user_id>/", following, name="following"),
    path("follow/<int:user_id>", follow, name="follow"),
    path("follow1/<int:user_id>", follow1, name="follow1"),
    path('skills/', SkillListCreateView.as_view(), name='skill-list-create'),
    path('api/skills/<int:id>/', SkillRetrieveUpdateDestroyView.as_view(), name='skills-detail'),

    # Volunteers
    path('volunteers/', VolunteerListCreateView.as_view(), name='volunteer-list-create'),
    path('profile-volunteer/', VolunteerDetailView.as_view(), name='profile-volunteer'),
    path('volunteer/<int:pk>/', VolunteerDetailView.as_view(), name='volunteer-detail'),
    path('api/volunteer/<int:id>/', VolunteerRetrieveUpdateDestroyView.as_view(),
         name='volunteer-detail-update-delete'),
    path('api/volunteer/<int:id>/add_skill/', AddSkillToVolunteerView.as_view(), name='add-skill-to-volunteer'),
    path('api/volunteer/<int:id>/remove_skill/', RemoveSkillFromVolunteerView.as_view(),
         name='remove-skill-from-volunteer'),

    # Organizations
    path('my-organizations/', my_organizations_view, name='my-organizations'),
    path('organizations/', OrganizationListCreateView.as_view(), name='organizations-list-create'),
    path('organizations/<int:pk>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('api/organization/<int:id>/', OrganizationRetrieveUpdateDestroyView.as_view(), name='update-organization'),
    path('profile-organization/<int:org_id>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('organization-memberships/', organization_memberships_view, name='organization-memberships'),

]