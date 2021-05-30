from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import *

from django.db.models import Q
from spellchecker import SpellChecker

import json

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, password_validation
from django.contrib import messages


from django.urls import reverse
from django.http import Http404, JsonResponse, HttpResponseRedirect

from django.core.paginator import Paginator

from .forms import PostForm, UserEditForm, BloggerEditForm
# Create your views here.
def home_view(request):
    top_posts = Post.objects.filter(published=True).order_by('-views')[:3]

    latest_posts = Post.objects.filter(published=True).order_by('-date_published')[:3]

    context = {'top_posts':top_posts, 'latest_posts':latest_posts}

    return render(request, 'blog/index.html',context)

def blog_view(request):

    latest_posts = Post.objects.filter(published=True).order_by('-date_published')

    paginator = Paginator(latest_posts,4)

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
        prev_post = Post.objects.filter(id__lt=post.id, published=True).order_by('-id').first()
    
    except Exception as e:
        prev_post = None

    try:
        next_post = Post.objects.filter(id__gt=post.id, published=True).order_by('id').first()

    except Exception as e:
        next_post = None
    
    latest_posts = Post.objects.filter(published=True).order_by('-date_published')[:3]

    comments = Comment.objects.filter(post=post).order_by("date_published")

    context = {'post':post, 'prev_post':prev_post, 'next_post':next_post, 'comments':comments,
                'latest_posts':latest_posts}
    return render(request, 'blog/post.html', context)

def search_view(request):
    
    search_term = request.GET.get('search')
    
    if search_term:
        posts = Post.objects.filter(
            Q(title__icontains=search_term)|
            Q(category__icontains=search_term)| 
            Q(description__contains=search_term)|
            Q(content__icontains=search_term),
            published=True)
        correct_term = ''
        if len(posts) <= 0:
            spell = SpellChecker()

            correct_term = spell.correction(search_term)

            posts = Post.objects.filter(
                Q(title__icontains=correct_term )|
                Q(category__icontains=correct_term )| 
                Q(description__contains=correct_term )|
                Q(content__icontains=correct_term ),
                published=True)
        
        if search_term == correct_term:
            correct_term = ''

        latest_posts = Post.objects.filter(published=True).order_by('-date_published')[:3]

        paginator = Paginator(posts,8)

        page = request.GET.get('page')

        try:
            page_posts = paginator.page(page)
        except:
            page_posts = paginator.page(1)

        context = {'posts':page_posts, 'search_term':search_term, 'correct_term':correct_term,'latest_posts':latest_posts}
        return render(request, 'blog/search.html',context)
    else:
        raise Http404

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
        username = request.POST.get('username').strip().lower()
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request, "Your account is not active!")
                return render(request, 'blog/login.html',{})
        else:
            messages.error(request, "Your username or password was incorrect!")
            return render(request, 'blog/login.html',{})
    else:
        return render(request, 'blog/login.html',{})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def user_registration(request):
    passwordValidations = password_validation.password_validators_help_texts()

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    
    if request.method == 'POST':
        username = request.POST.get('username').strip().lower()
        email = request.POST.get('email').strip().lower()
        fname = request.POST.get('fname').capitalize()
        lname = request.POST.get('lname').capitalize()
        password = request.POST.get('password')
        rpassword = request.POST.get('rpassword')

        if User.objects.filter(username=username).exists():
            messages.error(request,"Sorry! Username is already taken")
            return render (request, 'blog/registration.html',{'passwordValidations':passwordValidations})

        if User.objects.filter(email=email).exists():
            messages.error(request,"The email Id is already in use")
            return render (request, 'blog/registration.html',{'passwordValidations':passwordValidations})
        
        if password != rpassword:
            messages.error(request,"The passwords do not match")
            return render (request, 'blog/registration.html',{'passwordValidations':passwordValidations})
        
        try:
            password_validation.validate_password(password)
        except Exception as e:
            for error in e:
                messages.error(request, error)
            return render (request, 'blog/registration.html',{'passwordValidations':passwordValidations})

        user = User(is_superuser=False, is_staff=False, username=username, email=email, first_name=fname, last_name=lname)
        user.set_password(password)
        user.save()

        blogger = Blogger(user=user)
        blogger.create()
        blogger.save()

        return HttpResponseRedirect(reverse('login'))
        
    else:
        return render (request, 'blog/registration.html',{'passwordValidations':passwordValidations})

def profile_view(request, username):
    try:
        user = User.objects.get(username=username)
        blogger = Blogger.objects.get(user=user)
    except:
        raise Http404
    
    posts = Post.objects.filter(author=blogger, published=True).order_by("-date_published")
    context = {'blogger':blogger, 'posts':posts}
    return render(request, 'blog/profile.html', context)

@login_required
def edit_profile_view(request, username):
    try:
        user = User.objects.get(username=username)
        blogger = Blogger.objects.get(user=user)
    except:
        raise Http404

    if request.user != user:
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'GET':

        userform = UserEditForm(instance=user)
        bloggerform = BloggerEditForm(instance=blogger)

        context = {'userform':userform,'bloggerform':bloggerform, 'blogger':blogger}
        return render(request, 'blog/edit_profile.html', context)
    
    elif request.method == 'POST':
        if "username" and "first_name" and "last_name" and "bio" in request.POST:
            
            n_username = request.POST.get("username").strip().lower()
            fname = request.POST.get('first_name').strip().capitalize()
            lname = request.POST.get('last_name').strip().capitalize()
            bio = request.POST.get('bio').strip()

            if User.objects.filter(username=n_username).exists() and user.username != n_username:
                messages.error(request,"Sorry! Username is already taken")
                return HttpResponseRedirect(reverse('edit_profile',args=[username]))

            user.username = n_username
            user.first_name = fname
            user.last_name = lname
            user.save()

            blogger.bio = bio
            blogger.create()
            blogger.save()

            return HttpResponseRedirect(reverse('profile', args=[n_username]))
            
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
    
    content = data['form']['content']
    
    if request.user.is_authenticated:
        blogger = Blogger.objects.get(user=request.user)
        username = blogger.name
        email = blogger.email

        comment = Comment(post=post, author=blogger,name=username, email=email, content=content, anonymous=False)
    else:
        username = data['form']['username']
        email = data['form']['email']
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