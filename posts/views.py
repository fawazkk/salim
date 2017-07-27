
from django.shortcuts import get_object_or_404, render
from .models import Post
from .forms import PostForm
from django.contrib import messages
def post_list(request):
	obj_list = Post.objects.all()
	context = {
		"post_list": obj_list,
	}
	return render(request, 'post_list.html', context)
	
def post_detail(request, post_id):
	obj = get_object_or_404(Post, id=post_id)
	context = {
		"instance": obj,
		}

	return render (request, 'post_detail.html', context)

from .forms import PostForm

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Successfully Created!")
        return redirect("list")
    context = {
        "title": "Create",
        "form": form,
    }
    return render(request, 'post_create.html', context)

def post_update(request, post_id):
    instance = get_object_or_404(Post, id=post_id)
    form = PostForm(request.POST or None, instance = instance)
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
    

