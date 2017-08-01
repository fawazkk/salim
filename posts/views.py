
from django.shortcuts import get_object_or_404, render, redirect
from .models import Post
from .forms import PostForm, UserLogin, UserSignUp
from django.contrib import messages
from django.http import Http404
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login, logout


def post_list(request):
	today = timezone.now().date()
	obj_list = Post.objects.filter(draft=False).filter(publish__lte=today)

	query = request.GET.get("q")
	if query:
		obj_list = obj_list.filter(
			Q(title__icontains=query)|
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(author__first_name__icontains=query)|
			Q(author__last_name__icontains=query)
			).distinct()



	context = {
		"object_list": obj_list,
		"today":today,
	}
	return render(request, 'post_list.html', context)
	
def post_detail(request, slug):
	obj = get_object_or_404(Post, slug=slug)
	date = timezone.now().date()

	if obj.publish > date or obj.draft:
		if not(request.user.is_staff or request.user.is_superuser):
			raise Http404
			
	context = {
		"instance": obj,
		}

	return render (request, 'post_detail.html', context)

from .forms import PostForm

def post_create(request):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		obj.author = request.user
		obj.save()
		
		messages.success(request, "Successfully Created!")
		return redirect("list")
	context = {
		"title": "Create",
		"form": form,
	}
	return render(request, 'post_create.html', context)

def post_update(request, slug):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		form.save()
		messages.success(request, "Successfully Edited!")
		return redirect(instance.get_absolute_url())
	context = {
	"form":form,
	"instance": instance,
	"title": "Update",
	}
	return render(request, 'post_update.html', context)  

def post_delete(request, slug):
	if not (request.user.is_staff or request.user.is_superuser):
		raise Http404
	instance = get_object_or_404(Post, id=post_id)
	instance.delete()
	messages.success(request, "Successfully Deleted!")
	return redirect("list")


def usersignup(request):
	context = {}
	form= UserSignUp()
	context['form'] = form
	if request.method == "POST":
		form = UserSignUp(request.POST)
		if form.is_valid():

			user = form.save(commit=False)
			username = user.username
			password = user.password
			user.set_password(password)
			user.save()
			auth_user = authenticate(username=username, password=password)
			login(request, auth_user)

			return redirect("posts:list")
		messages.error(request, form.errors)
		return redirect("posts:signup")
	return render(request, 'signup.html', context)


def userlogin(request):
	context = {}
	form = UserLogin()
	context['form'] = form
	if request.method == "POST":
		form = UserLogin(request.Post)
		if form.is_valid():

			username = forms.cleaned_data['username']
			password = forms.cleaned_data['password']

			auth_user = authenticate(username=username, password=password)
			if auth_user is not None:
				login(request, auth_user)
				return redirect("post:list")

			messages.warning(request, "Wrong username/password combination. Please try agaon.") 
			return redirect("posts:login")
		messages.warning(request, form.errors)
		return redirect("posts:login")
	return render(request, 'login.html', context)	


def userlogout(request):
	logout(request)
	return redirect("posts;login")












