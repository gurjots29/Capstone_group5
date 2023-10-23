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
    path('', include('apps.users.urls')),
    path('post/', include('apps.post.urls')),
<<<<<<< HEAD
    path('event/', include('apps.event.urls')),
=======
>>>>>>> 9fe5041adb8bd46e6986e2837e2f09061ff40e0d
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


