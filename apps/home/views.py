from django.shortcuts import render
from apps.post.models import Post 
from apps.event.models import Event
from django.http import JsonResponse
from django.db.models import Q
from apps.users.models import Volunteer, Organization
from django.utils import timezone
from django.db.models import Value, CharField

# Create your views here.

#def home(request):
 #   return render(request, 'home.html')


def home(request):
    posts = Post.objects.all().order_by('-created_at').select_related('user')
    # Obtener los próximos eventos
    upcoming_events = Event.objects.filter(start_time__gt=timezone.now()).order_by('start_time')[:5]  # Ejemplo: los 5 próximos eventos

    context = {
        'posts': posts,
        'upcoming_events': upcoming_events,
        
    }

    return render(request, 'home.html', context)


def search_api(request):
    query = request.GET.get('term', '')  # 'term' es el parámetro comúnmente usado por plugins de autocompletar

    # Búsqueda en el modelo 'Volunteer'
    volunteers = Volunteer.objects.filter(
        Q(user__first_name__icontains=query) | 
        Q(user__last_name__icontains=query) | 
        Q(bio__icontains=query) | 
        Q(phone_number__icontains=query) | 
        Q(headline__icontains=query)
    )

    # Búsqueda en el modelo 'Organization'
    organizations = Organization.objects.filter(
        Q(name__icontains=query) | 
        Q(description__icontains=query) | 
        Q(email__icontains=query) | 
        Q(phone_number__icontains=query)
    )

    results = {
    'volunteers': list(volunteers.values('id', 'user__first_name', 'user__last_name', 'bio').annotate(type=Value('volunteer', output_field=CharField()))),
    'organizations': list(organizations.values('id', 'name', 'description').annotate(type=Value('organization', output_field=CharField())))
     }
    return JsonResponse(results)
