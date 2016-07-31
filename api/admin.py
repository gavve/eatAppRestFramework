from django.contrib import admin
from .models import Event, ParticipantsInEvent
# Register your models here.

class ParticipantsInEventInline(admin.TabularInline):
    model = ParticipantsInEvent
    extra = 2 # how many rows to show

class EventAdmin(admin.ModelAdmin):
    inlines = (ParticipantsInEventInline,)

admin.site.register(Event, EventAdmin)

