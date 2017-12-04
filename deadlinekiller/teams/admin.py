from django.contrib import admin

from .models import Team


class TeamAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug',]
	list_filter = ['name', 'slug', ]
	search_fields = ['name',]
	prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Team, TeamAdmin)