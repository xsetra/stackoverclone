from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from .models import Post, Comment
from .forms import PostForm, CommentForm, CommentOfCommentForm
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
import json


def profile_api(request):
    if request.method != 'POST':
        resp = HttpResponse("Method not allowed")
        resp.status_code = 405
        return resp
    else:
        body = str(request.body)
        username = body.split("=")[2][:-1]
        posts = Post.objects.filter(yazar__username=username)
        l = [p.as_dict() for p in posts]
        response_text = json.dumps(l)
        resp = HttpResponse(response_text)
        return resp

@login_required
def add_reply(request, pk, c_id):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentOfCommentForm(request.POST)
        if form.is_valid():
            parent_comment = Comment.objects.get(id=c_id)
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.parent_comment = parent_comment
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentOfCommentForm()
    return render(request, 'post/add_reply.html', {'form': form})


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def post_list(request):
    #posts = Post.objects.filter(yayinlanma_tarihi__lte=timezone.now()).order_by('yayinlanma_tarihi')
    posts = Post.objects.all().order_by('yayinlanma_tarihi')
    return render(request, 'post/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    print(post)
    return render(request, 'post/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.yazar = request.user
            post.yayinla()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.yazar = request.user
            post.yayinla()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'post/post_edit.html', {'form': form})


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'post/add_comment_to_post.html', {'form': form})


@login_required
def profile(request):
    posts = Post.objects.filter(yazar=request.user)
    comments = Comment.objects.filter(author=request.user)
    posts_comm = [p.post for p in comments]
    commented_posts = set(posts_comm)
    return render(request, 'profile.html', {'posts': posts, 'commented_posts': commented_posts})
