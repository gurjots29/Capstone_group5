"""
URL configuration for volunteer_platform project.

"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', include('apps.home.urls')),
    path('admin/', admin.site.urls),
    path('', include(('apps.users.urls', 'users'), namespace='users')),
    path('post/', include('apps.post.urls')),
   # path('event/', include('apps.event.urls')),
   path('event/', include(('apps.event.urls', 'event'), namespace='event')),
    path('auth/', include('social_django.urls', namespace='social')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


