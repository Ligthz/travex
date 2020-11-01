from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('mobile-login')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			roles = []
			if request.user.is_superuser:
				return view_func(request, *args, **kwargs)
			if request.user.is_admin:
				roles.append('admin')
			if request.user.is_staff:
				roles.append('staff')

			if request.user.is_active:
				for role in roles:
					if role in allowed_roles:
						return view_func(request, *args, **kwargs)
			return HttpResponse('You are not authorized to view this page')
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.is_staff or request.user.is_admin:# or request.user.is_manager or request.user.is_staff or request.user.is_salesman:
			return view_func(request, *args, **kwargs)

		else:
			return redirect('mobile-home')


	return wrapper_function

def active_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		if request.user.is_active:# or request.user.is_manager or request.user.is_staff or request.user.is_salesman:
			return view_func(request, *args, **kwargs)

		else:
			return redirect('mobile-login')


	return wrapper_function