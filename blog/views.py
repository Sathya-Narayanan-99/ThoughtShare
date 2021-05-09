from django.shortcuts import render
from .models import *

import json

from django.shortcuts import redirect
from django.urls import reverse
from django.http import Http404, JsonResponse, HttpResponseRedirect

# Create your views here.
def home_view(request):
    return render(request, 'blog/index.html',{})

def blog_view(request):
    return render(request, 'blog/blog.html', {})

def post_view(request, pk):

    try:
        post = Post.objects.get(id=pk)
        post.views += 1
        post.save()
    except:
        raise Http404

    try:
        prev_post = Post.objects.get(id=pk-1)
    except Exception as e:
        prev_post = None
        print(e)

    try:
        next_post = Post.objects.get(id=pk+1)

    except Exception as e:
        next_post = None
        print(e)
    
    latest_posts = Post.objects.order_by('-date_published')[:3]

    comments = Comment.objects.filter(post=post)

    context = {'post':post, 'prev_post':prev_post, 'next_post':next_post, 'comments':comments,
                'latest_posts':latest_posts}
    return render(request, 'blog/post.html', context)

def add_comment(request):
    
    data = json.loads(request.body)

    pk = data['postId']
    print(pk, data)
    try:
        post = Post.objects.get(id=pk)
    except Exception as e:
        print(e)
    
    username = data['form']['username']
    email = data['form']['email']
    content = data['form']['content']

    comment = Comment(post=post, name=username, email=email, content=content)
    comment.save()
    return JsonResponse("comment was added", safe=False)