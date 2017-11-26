from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify

from .forms import DeadlineForm
from .models import Deadline


@login_required
def deadline_list(request):
	deadline_list = Deadline.objects.filter(author=request.user)
	deadlines_total = deadline_list.count()
	paginator = Paginator(deadline_list, 10) 
	page = request.GET.get('page')
	try:
		deadlines = paginator.page(page)
	except PageNotAnInteger:
        # If page is not an integer, deliver first page.
		deadlines = paginator.page(1)
	except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
		deadlines = paginator.page(paginator.num_pages)
	return render(request, 'deadlines/deadline_list.html', { 'deadlines' : deadlines,
															 'deadlines_total' : deadlines_total,
															 'page' : page })


@login_required
def deadline_detail(request, pk, slug):
	deadline = get_object_or_404(Deadline, pk=pk, slug=slug)
	return render(request, 'deadlines/deadline_detail.html', {'deadline' : deadline})


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
			messages.success(request, 'New deadline was created. Tick tock, tick tock...')
			return redirect('deadlines:deadline_list')

	else:
		deadline_form = DeadlineForm()
	return render(request, 'deadlines/deadline_create.html', {'deadline_form' : deadline_form})


@login_required
def deadline_update(request, pk, slug):
	deadline = get_object_or_404(Deadline, pk=pk, slug=slug)
	if request.method == 'POST':
		deadline_form = DeadlineForm(instance=deadline, data=request.POST)
		if deadline_form.is_valid():
			deadline_form.save()
			messages.success(request, '{} deadline was updated successfully.'.format(deadline.name))
			return redirect(deadline)
	else:
		deadline_form = DeadlineForm(instance=deadline)

	return render(request, 'deadlines/deadline_update.html', {'deadline' : deadline,
															  'deadline_form' : deadline_form})


@login_required
def deadline_delete(request, pk, slug):
	deadline = get_object_or_404(Deadline, pk=pk, slug=slug)
	deadline.delete()
	messages.success(request, '{} deadline was deleted successfully.'.format(deadline.name))
	return redirect('deadlines:deadline_list')
	