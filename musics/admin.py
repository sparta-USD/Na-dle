from django.contrib import admin
from .models import Music
from musics.models import Review

# Register your models here.
admin.site.register(Music)
admin.site.register(Review)
