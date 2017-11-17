from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Deadline


@login_required
def deadline_list(request):
	deadlines = Deadline.objects.filter(author=request.user)
	return render(request, 'deadlines/deadline_list.html', { 'deadlines' : deadlines })
