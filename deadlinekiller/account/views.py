from django.contrib.auth import authenticate, login 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView

from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile



class ProfileView(LoginRequiredMixin, DetailView):
	model = Profile
	template_name = 'account/profile_detail.html'



def user_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(username=cd['username'],
								password=cd['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponse('Authentication succeeded')
				else:
					return HttpResponse('Account is blocked')
			else:
				return HttpResponse('Wrong authentication data')
	else:
		form = LoginForm()
	return render(request, 'account/login.html', {'form' : form})



def register(request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST) 
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			# Set given password
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			profile = Profile.objects.create(user=new_user)
			return render(request, 'account/register_done.html', { 'new_user' : new_user })
	else:
		user_form = UserRegistrationForm()
	return render(request, 'account/register.html', { 'user_form': user_form })


@login_required
def edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user,
								 data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile,
									   data=request.POST,
									   files=request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)
	return render(request, 'account/edit.html', { 'user_form' : user_form,
								 				  'profile_form' : profile_form })











# TEST VIEW
def test_home(request):
	return render(request, 'account/test_home.html', {})
