from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login 

from .forms import LoginForm, UserRegistrationForm


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
			return render(request, 'account/register_done.html', { 'new_user' : new_user })
	else:
		user_form = UserRegistrationForm()
	return render(request, 'account/register.html', { 'user_form': user_form })








# TEST VIEW
def test_home(request):
	return HttpResponse('test_home page loaded')
