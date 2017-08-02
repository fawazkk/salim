from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    slug = models.SlugField(unique=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="post_images")
    author = models.ForeignKey(User, default=1)
    draft = models.BooleanField(default=False)
    publish = models.DateField()
    def __str__(self):
    	return self.title


    def get_absolute_url(self):
        return reverse("detail", kwargs={"slug": self.slug})


def create_slug(instance, new_slug=None):
	slug=slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug)
	exists = qs.exists()
	if exists: 
		new_slug = "%s-%s"%(slug, instance.id)
		return create_slug(instance, new_slug=new_slug)
	return slug 


def post_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		slug=slugify(instance.title)
		qs = Post.objects.filter(slug=slug).order_by("-id")
		exists = qs.exists()
		if exists:
			slug = "%s-%s"%(slug, instance.id)
		instance.slug = slug
		instance.save()

post_save.connect(post_reciever, sender=Post)


class Like(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    











