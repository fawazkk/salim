
from django.shortcuts import get_object_or_404, render
from .models import Post

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
