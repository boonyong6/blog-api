from django.http import Http404
from django.shortcuts import render
from .models import Post


# Create your views here.
def post_list(request):
    posts = Post.published.all()
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, id):
    try:
        post = Post.publish.get(id=id)
    except Post.DoesNotExist:
        raise Http404("No Post found.")

    return render(request, "blog/post/detail.html", {"posts": post})
