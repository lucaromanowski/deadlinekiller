from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.text import slugify

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
			# Assigne logged in user to a deadline (as an author)
			new_form.author = request.user
			# Create a slug from name field
			new_form.slug = slugify(new_form.name)
			new_form.save()
			return redirect('deadlines:deadline_list')

	else:
		deadline_form = DeadlineForm()
	return render(request, 'deadlines/deadline_create.html', {'deadline_form' : deadline_form})
	