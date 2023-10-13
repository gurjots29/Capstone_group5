<<<<<<< HEAD
from django.contrib import admin

# Register your models here.
=======

from django.contrib import admin

from apps.users.models import Comment, Post

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
>>>>>>> 5afe1c1 (Pushing for POST API and Comments API)
