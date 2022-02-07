from django.contrib import admin
from .models import Team
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'position')
    list_filter = ("name", "position")
    search_fields = ['name', 'slug', 'position']
    prepopulated_fields = {'slug': ('name',)}
  
admin.site.register(Team, TeamAdmin)