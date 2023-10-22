from django.urls import path 

from .views import EventViewSet, RegistrationEventsViewSet, ProgramViewSet
urlpatterns = [
   path('events/', EventViewSet.as_view(), name='api_createevent'),
   path('registration-events/', RegistrationEventsViewSet.as_view(), name='api_registrationevent'),
   path('programs/', ProgramViewSet.as_view(), name='api_programs'),
]
