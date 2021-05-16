from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *

import json

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate

from django.urls import reverse
from django.http import Http404, JsonResponse, HttpResponseRedirect

from django.core.paginator import Paginator

from .forms import PostForm
# Create your views here.
def home_view(request):
    top_posts = Post.objects.filter(published=True).order_by('-views')[:3]

    latest_posts = Post.objects.filter(published=True).order_by('-date_published')[:3]

    context = {'top_posts':top_posts, 'latest_posts':latest_posts}

    return render(request, 'blog/index.html',context)

def blog_view(request):

    latest_posts = Post.objects.filter(published=True).order_by('-date_published')

    paginator = Paginator(latest_posts,2)

    page = request.GET.get('page')
    
    try:
        page_posts = paginator.page(page)
    except:
        page_posts = paginator.page(1)

    context = {'posts':page_posts, 'latest_posts':latest_posts[:3]}
    return render(request, 'blog/blog.html', context)

def post_view(request, pk):

    try:
        post = Post.objects.get(id=pk, published=True)
        
        if request.user != post.author.user:
            post.views += 1
            post.save()

    except:
        raise Http404

    try:
        prev_post = Post.objects.get(id=pk-1)
    except Exception as e:
        prev_post = None

    try:
        next_post = Post.objects.get(id=pk+1)

    except Exception as e:
        next_post = None
    
    latest_posts = Post.objects.filter(published=True).order_by('-date_published')[:3]

    comments = Comment.objects.filter(post=post)

    context = {'post':post, 'prev_post':prev_post, 'next_post':next_post, 'comments':comments,
                'latest_posts':latest_posts}
    return render(request, 'blog/post.html', context)

@login_required
def new_post_view(request):
    
    if request.method == 'GET':
    
        form = PostForm()
        context = {'form':form}
        return render(request, 'blog/new_post.html',context)
    
    else:

        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            blogger = Blogger.objects.get(user = request.user)

            post.author = blogger
            post.publish()
            post.save()

        return HttpResponseRedirect(reverse('post',args= [post.id]))

@login_required
def draft_view(request):
    author = Blogger.objects.get(user=request.user)
    
    drafts = Post.objects.filter(author=author, published=False).order_by("-id")
    latest_posts = Post.objects.filter(published=True).order_by("-date_published")[:3]

    context = {'posts':drafts, 'latest_posts':latest_posts}

    return render(request, 'blog/draft.html', context)

@login_required
def edit_post_view(request,pk):
    post = get_object_or_404(Post, id=pk)

    if request.user == post.author.user:

        if post.title or post.post_pic or post.category or post.content:
            form = PostForm(instance=post)
            context = {'form':form, 'post':post}
            return render(request, 'blog/edit.html', context)
        
    else:
        raise Http404

@login_required
def preview_post_view(request,pk):
    try:
        post = Post.objects.get(id=pk, published=False)
    except:
        raise Http404

    if request.user == post.author.user:
        latest_posts = Post.objects.filter(published=True).order_by('-date_published')[:3]

        context = {'post':post, 'latest_posts':latest_posts}

        return render(request, 'blog/preview.html', context)
    else:
        raise Http404

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("User not active")
        else:
            return HttpResponse("Invalid Credentials")
    else:
        return render(request, 'blog/login.html',{})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


#--------------------------------------------------------------------------------------------------
#
#--------------------------------------------------------------------------------------------------

def add_comment(request):
    
    data = json.loads(request.body)

    pk = data['postId']

    try:
        post = Post.objects.get(id=pk)
    except Exception as e:
        print("Exception while adding comment",e)
    
    if request.user.is_authenticated:
        blogger = Blogger.objects.get(user=request.user)
        username = blogger.name
        email = blogger.email
    else:
        username = data['form']['username']
        email = data['form']['email']
    
    content = data['form']['content']

    comment = Comment(post=post, name=username, email=email, content=content)
    comment.save()
    return JsonResponse("comment was added", safe=False)

@login_required
def add_to_draft(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)

            author = Blogger.objects.get(user = request.user)
            post.author = author
            post.save()

            if 'preview-button' in request.POST:
                return HttpResponseRedirect(reverse("preview",args=[post.id]))
            else:
                return HttpResponseRedirect(reverse('draft'))
    else:
        raise Http404

@login_required
def publish_post(request, pk):
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=pk)
        except:
            raise Http404
        
        if request.user == post.author.user:
            post.publish()
            post.save()

            return HttpResponseRedirect(reverse('post',args=[post.id]))
        else:
            raise Http404
    else:
        raise Http404

@login_required
def add_edit_draft(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=pk)

        if request.user == post.author.user:
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()

                if "preview-button" in request.POST:
                    return HttpResponseRedirect(reverse('preview', args=[pk]))
                else:
                    return HttpResponseRedirect(reverse('draft'))
            else:
                raise Http404