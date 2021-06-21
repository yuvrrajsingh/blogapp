import datetime

from django.shortcuts import render, HttpResponseRedirect
from .forms import SignupForm, LoginForm, PostForm
from .models import Post, User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from datetime import date, datetime
# Home
def home(request):
    posts = Post.objects.all()
    return render(request, 'myblog/home.html', {'posts': posts})

# About
def about(request):
    return render(request, 'myblog/about.html')

# Contact
def contact(request):
    return render(request, 'myblog/contact.html')

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        full_name = user.get_full_name()
        username = user.get_username()
        posts = Post.objects.filter(user__username=username)
        all_post = Post.objects.all()
        gps = user.groups.all()
        return render(request, 'myblog/dashboard.html', {'posts':posts, 'full_name':full_name, 'groups':gps, 'all_posts': all_post})
    else:
        return HttpResponseRedirect('/login/')

# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

# Signup
def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! You have become an Author')
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)

        form = SignupForm()
    else:
        form = SignupForm()

    return render(request, 'myblog/signup.html', {'form':form})

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
                    if request.user.is_superuser:
                        return HttpResponseRedirect('/admin/')
                    else:
                        messages.success(request, 'Logged in Successfully!')
                        return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'myblog/login.html', {'form':form})

    else:
        return HttpResponseRedirect('/dashboard/')


# Add new post
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                # form.save()
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                today_date = date.today()
                now = datetime.now()
                tym = now.strftime("%H:%M:%S")
                pst = Post(title=title, desc=desc, date=today_date, time=tym, user=request.user)
                pst.save()

                return HttpResponseRedirect('/dashboard/')
        else:
            form = PostForm()
        return render(request, 'myblog/addpost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')

# Add Update post
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request, 'Updated Successfully!!')
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)

        return render(request, 'myblog/updatepost.html', {'form':form})
    else:
        return HttpResponseRedirect('/login/')

# Delete post
def delete(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')