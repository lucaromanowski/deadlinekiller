from django.contrib import admin

from .models import Deadline


class DeadlineAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug', 'author', 'deadline_date', 'created', 'updated', 'priority')
	list_filter = ('name', 'slug', 'author', 'deadline_date', 'created', 'updated', 'priority')
	search_fields = ('name', 'description')
	prepopulated_fields = {'slug' :('name',)}

admin.site.register(Deadline, DeadlineAdmin)

