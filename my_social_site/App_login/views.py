from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from App_login.forms import CreateNewUser,EditProfile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .models import Follow, UserProfile
from App_posts.forms import NewPost
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def signup_form(request):
    form=CreateNewUser()
    registered=False
    if request.method=='POST':
        form=CreateNewUser(data=request.POST)
        if form.is_valid():
            user=form.save()
            registered=True
            user_profile=UserProfile(user=user)
            user_profile.save()
            return HttpResponseRedirect(reverse('App_login:login'))
    return render(request,'App_login/signup.html',context={'form':form})

def login_form(request):
    form=AuthenticationForm()
    if request.method == 'POST':
        form=AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('App_post:home'))

    return render(request, 'App_login/login.html', context={'form':form})

@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('App_login:login'))


@login_required
def edit_profile(request):
    current_user=UserProfile.objects.get(user=request.user)
    form=EditProfile(instance=current_user)
    if request.method == 'POST':
        form=EditProfile(request.POST,request.FILES,instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form = EditProfile(instance=current_user)
            return HttpResponseRedirect(reverse('App_login:user'))

    return render(request,'App_login/profile.html',context={'form':form})


@login_required
def user_profile(request):
    form=NewPost()
    if request.method=='POST':
        form=NewPost(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            return HttpResponseRedirect(reverse('home'))
    return render(request,'App_login/user.html',context={'form':form})

@login_required
def user_other(request,username):
    new_user=User.objects.get(username=username)
    already_followed=Follow.objects.filter(follower=request.user,following=new_user)
    if new_user==request.user:
        return HttpResponseRedirect(reverse('App_login:user'))
    return render(request,'App_login/user_other.html',context={'new_user':new_user,'already_followed':already_followed})


@login_required
def follow(request,username):
    following_user=User.objects.get(username=username)
    follower_user=request.user
    already_followed=Follow.objects.filter(follower=follower_user,following=following_user)
    if not already_followed:
        followed_user=Follow(follower=follower_user,following=following_user)
        followed_user.save()
    return HttpResponseRedirect(reverse('App_login:user_other',kwargs={'username':username}))

@login_required
def unfollow(request,username):
    following_user=User.objects.get(username=username)
    follower_user=request.user
    already_followed=Follow.objects.filter(follower=follower_user,following=following_user)
    already_followed.delete()
    return HttpResponseRedirect(reverse('App_login:user_other',kwargs={'username':username}))


