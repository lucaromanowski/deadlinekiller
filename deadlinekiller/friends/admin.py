from django.contrib import admin

from .models import Connection

class ConnectionAdmin(admin.ModelAdmin):
	list_display = ['creator', 'following', 'created', 'accepted']
	search_fields = ['creator', 'following', 'created', 'accepted']

admin.site.register(Connection, ConnectionAdmin)
