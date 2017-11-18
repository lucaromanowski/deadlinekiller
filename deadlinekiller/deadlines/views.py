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
		current_user = User.objects.get(username=request.user)
		deadline_form.author = current_user
		#deadline_form.author = request.user
		#deadline_form.clean_author()
		if deadline_form.is_valid():
			deadline_form.save(commit=False)
			
			deadline_form.save()

	else:
		deadline_form = DeadlineForm()
	return render(request, 'deadlines/deadline_create.html', {'deadline_form' : deadline_form})
	