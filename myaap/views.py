from django.shortcuts import render, HttpResponseRedirect
from . forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group


# Home
def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html',{'posts':posts})

def home_slug(request, slug):
    post = Post.objects.get(slug=slug)
    return render(request, 'blog.html',{'post':post})

# About
def about(request):
    return render(request, 'about.html')

# Contact
def contact(request):
    return render(request, 'contact.html')

#DashBoard
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()

        return render(request, 'dashboard.html', {'posts':posts, 'full_name': full_name, 'groups':gps})
    else:
        return HttpResponseRedirect('/login/')

# Signup
def user_signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard/')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Congratulation! You have become an auther.')
                user = form.save()
                group = Group.objects.get(name='Author')
                user.groups.add(group)
        else:
            form = SignUpForm()
        return render(request, 'signup.html',{'form':form})

# Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')
# Logout
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login/')


# Add Post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'addpost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')


# Update Post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')


# Delete Post
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard')
    else:
        return HttpResponseRedirect('/login/')
