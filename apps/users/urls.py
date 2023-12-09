from django.urls import path
from .views import (user_logout,user_login,forgot_password_view,profile_organizations_view, 
                    SkillRetrieveUpdateDestroyView, VolunteerRetrieveUpdateDestroyView, 
                    BadgeListCreateView, SkillListCreateView, VolunteerListCreateView, 
                    OrganizationListCreateView,VolunteerDetailView, AddSkillToVolunteerView,
    RemoveSkillFromVolunteerView, my_organizations_view ,OrganizationDetailView,
    OrganizationRetrieveUpdateDestroyView, organization_memberships_view,user_signup, update_profile_picture,
    update_background_image,update_profile_logo,update_obackground_image,AddInterestToVolunteerView, 
    RemoveInterestFromVolunteerView, AddInterestToOrganizationView, RemoveInterestFromOrganizationView,
    VolunteerMatchView,VolunteerRelationships,unfollow_volunteer,follow_volunteer,follow_organization,unfollow_organization,
    skills_admin_view, AddSkillView, AddInterestView, interest_admin_view,AddOrganizationMembershipView,accept_membership_view,
    SuggestedVolunteerList, like_post, is_liked, VolunteerDetailView2,
)
app_name = 'users'

urlpatterns = [
    #Users
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='user_logout'),
    path('badges/', BadgeListCreateView.as_view(), name='badge-list-create'),
    path('forgot-password/', forgot_password_view, name='forgot-password'),
    path('sign-up/', user_signup, name='sign-up'),

    path('skills/', SkillListCreateView.as_view(), name='skill-list-create'),
    path('api/skills/<int:id>/', SkillRetrieveUpdateDestroyView.as_view(), name='skills-detail'),

    #Volunteers
    path('volunteers/', VolunteerListCreateView.as_view(), name='volunteer-list-create'),
    path('profile-volunteer/', VolunteerDetailView.as_view(), name='profile-volunteer'),
    path('volunteer/<int:pk>/', VolunteerDetailView.as_view(), name='volunteer-detail'),  
    path('api/volunteer/<int:id>/add_skill/', AddSkillToVolunteerView.as_view(), name='add-skill-to-volunteer'),
    path('api/volunteer/<int:id>/remove_skill/', RemoveSkillFromVolunteerView.as_view(), name='remove-skill-from-volunteer'),
    path('api/volunteer/<int:id>/update_profile_picture/', update_profile_picture, name='update-profile-picture'),
    path('api/volunteer/<int:id>/update_background_image/', update_background_image, name='update-background-image'),
    path('api/volunteer/<int:id>/add_interest/', AddInterestToVolunteerView.as_view(), name='add-intereest-to-volunteer'),
    path('api/volunteer/<int:id>/remove_interest/', RemoveInterestFromVolunteerView.as_view(), name='remove-interest-from-volunteer'),
    path("relationships/", VolunteerRelationships, name="relationships"),
    path('unfollow_volunteer/<int:volunteer_id>/', unfollow_volunteer, name='unfollow-volunteer'),
    path('follow_volunteer/<int:volunteer_id>/', follow_volunteer, name='follow-volunteer'),
    path('api/suggestions/', SuggestedVolunteerList.as_view(), name='suggested_volunteers'),
    path('like_post/<int:post_id>/', like_post, name='like_post'),
    path('is_liked/<int:post_id>/', is_liked, name='is_liked'),

    #Organizations
    path('my-organizations/', my_organizations_view, name='my-organizations'),
    path('organizations/', OrganizationListCreateView.as_view(), name='organizations-list-create'),
    path('organizations/<int:pk>/', OrganizationDetailView.as_view(), name='organization-detail'),
    path('api/organization/<int:id>/', OrganizationRetrieveUpdateDestroyView.as_view(), name='update-organization'),
    path('api/organization/<int:id>/update_profile_logo/', update_profile_logo, name='update-profile-logo'),
    path('api/organization/<int:id>/update_background_image/', update_obackground_image, name='update-obackground-image'),
    path('api/organization/<int:id>/add_interest/', AddInterestToOrganizationView.as_view(), name='add-intereest-to-organization'),
    path('api/organization/<int:id>/remove_interest/', RemoveInterestFromOrganizationView.as_view(), name='remove-interest-from-organization'),
    path('organization-match/', VolunteerMatchView.as_view(), name='organization-match'),
    path('organization-match/subscribe/<int:organization_id>/', VolunteerMatchView.as_view(), name='organization-subscribe'),

    path('unfollow_organization/<int:organization_id>/', unfollow_organization, name='unfollow-organization'),
    path('organization/<int:organization_id>/follow', follow_organization, name='follow-organization'),
    


    path('profile-organization/<int:pk>/', OrganizationDetailView.as_view(), name='profile-organization'),
    path('organization-memberships/', organization_memberships_view, name='organization-memberships'),
     path('accept-membership/<int:membership_id>/', accept_membership_view, name='accept-membership'),

    #Administration
    path('skills-admin/', skills_admin_view, name='skills-admin'),
    path('add-skill/', AddSkillView.as_view(), name='add-skill'),

    path('interest-admin/', interest_admin_view, name='interest-admin'),
    path('add-interest/', AddInterestView.as_view(), name='add-interest'),


]
