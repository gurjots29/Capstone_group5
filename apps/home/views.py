from django.shortcuts import render
from apps.post.models import Post 
from apps.event.models import Event
from django.utils import timezone
# Create your views here.

#def home(request):
 #   return render(request, 'home.html')


def home(request):
    posts = Post.objects.all().order_by('-created_at').select_related('user')
    # Get upcoming events
    upcoming_events = Event.objects.filter(start_time__gt=timezone.now()).order_by('start_time')[:5]  # Ejemplo: los 5 próximos eventos

    context = {
        'posts': posts,
        'upcoming_events': upcoming_events,
    }

    return render(request, 'home.html', context)
