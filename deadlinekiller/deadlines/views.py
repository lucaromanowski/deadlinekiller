from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from .forms import DeadlineForm
from .models import Deadline


@login_required
def deadline_list(request):
	deadlines = Deadline.objects.filter(author=request.user)
	return render(request, 'deadlines/deadline_list.html', { 'deadlines' : deadlines })


@login_required
def deadline_create(request):
	if request.method == 'POST':
		deadline_form = DeadlineForm(request.POST)
		
		if deadline_form.is_valid():
			new_form = deadline_form.save(commit=False)
			new_form.author = request.user
			new_form.save()

	else:
		deadline_form = DeadlineForm()
	return render(request, 'deadlines/deadline_create.html', {'deadline_form' : deadline_form})
	