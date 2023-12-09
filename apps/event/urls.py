from django.urls import path 

from .views import (EventRegisterView,EventUnregisterView, EventRetrieveUpdateView, EventViewSet, RegistrationEventsViewSet, ProgramViewSet,
                   events_management_view,CreateEventView,events_view)

urlpatterns = [
   path('events/', EventViewSet.as_view(), name='api_createevent'),
  

   path('registration-events/', RegistrationEventsViewSet.as_view(), name='api_registrationevent'),
   path('programs/', ProgramViewSet.as_view(), name='api_programs'),


   path('new/', CreateEventView.as_view(), name='create-event'),
   path('events-management/', events_management_view, name='events-management'),
   path('view-events', events_view, name='view-events'),

   path('events/<int:pk>/', EventRetrieveUpdateView.as_view(), name='event-detail'),
   path('events/<int:event_id>/register/', EventRegisterView.as_view(), name='event-register'),
   path('events/<int:event_id>/unregister/', EventUnregisterView.as_view(), name='event-unregister'),

]
