from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login 
from .forms import LoginForm

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









# TEST VIEW
def test_home(request):
	return HttpResponse('test_home page loaded')
