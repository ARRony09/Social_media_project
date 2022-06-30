from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse

from App_login.models import Follow
from .models import Like, Posts
from App_posts.forms import UserComment

# Create your views here.


@login_required
def home(request):
    following_list=Follow.objects.filter(follower=request.user)
    posts=Posts.objects.filter(author__in=following_list.values_list('following'))
    liked_post=Like.objects.filter(user=request.user)
    liked_post_list=liked_post.values_list('post',flat=True)
    if request.method=='GET':
        search=request.GET.get('search','')
        result=User.objects.filter(username__icontains=search)
    return render(request,'App_posts/home.html',context={'search':search,'result':result,'posts':posts,'liked_post_list':liked_post_list})

@login_required
def like(request,pk):
    post=Posts.objects.get(pk=pk)
    already_liked=Like.objects.filter(post=post,user=request.user)
    if not already_liked:
        liked_post=Like(post=post,user=request.user)
        liked_post.save()
    return HttpResponseRedirect(reverse('home'))

@login_required
def unlike(request,pk):
    post=Posts.objects.get(pk=pk)
    already_liked=Like.objects.filter(post=post,user=request.user)
    already_liked.delete()
    return HttpResponseRedirect(reverse('home'))

@login_required
def comment(request,pk):
    post=Posts.objects.get(pk=pk)
    comment_form=UserComment()
    if request.method=='POST':
        comment_form=UserComment(data=request.POST)
        if comment_form.is_valid():
            comment=comment_form.save(commit=False)
            comment.user=request.user
            comment.post=post
            comment.save()
            return HttpResponseRedirect(reverse('App_post:comment',kwargs={'pk':pk}))


    return render(request,'App_posts/comment.html',context={'post':post,"comment_form":comment_form})