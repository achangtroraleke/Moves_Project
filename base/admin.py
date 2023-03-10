from django.contrib import admin

# Register your models here.

from .models import Poll, Venue, User, Option

admin.site.register(Poll)
admin.site.register(Venue)
admin.site.register(User)
admin.site.register(Option)