
from django.contrib import admin
from .models import User, MartialArt, Movement, PracticeSession, ProgressHistory

@admin.register(MartialArt)
class MartialArtAdmin(admin.ModelAdmin):
    list_display = ("name", "description")


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ("name", "martial_art_id", "tutorial")


