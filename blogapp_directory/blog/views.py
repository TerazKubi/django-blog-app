from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .forms import NewUserForm, BlogPostForm, CommentForm
from .models import BlogPost, Comment

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.db.models import Count


def index(request):
    posts = BlogPost.objects.annotate(comment_count=Count('comments')).order_by('-created_at')

    return render(request, 'blog/index.html', {'posts': posts})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("/")
        
        messages.error(request, "Unsuccessful registration. Invalid information.")

    form = NewUserForm()
    return render (request=request, template_name="blog/register.html",context={"register_form":form})


def login_request(request):
    if request.user.is_authenticated:
        return redirect("/")
    
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Login fail.")
            
        else:
            messages.error(request, "Login fail. Invalid form")


    form = AuthenticationForm()
    return render(request=request, template_name="blog/login.html", context={"login_form":form})


def logout_request(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('/')
    
    return redirect('/login')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  
            post.author = request.user      
            post.save()                     
            return redirect('index')        
    else:
        form = BlogPostForm()
    return render(request, 'blog/post_form.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    if post.author != request.user:
        return redirect('post_detail', post_id=post.id)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.id)
    else:
        form = BlogPostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)

    if post.author != request.user:
        return redirect('post_detail', pk=post.id)

    if request.method == 'POST':
        post.delete()
        return redirect('index')

    return render(request, 'blog/delete_post.html', {'post': post})


def post_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect('post_detail', post_id=post.id)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'blog/post.html', {'post': post, 'comments': comments, 'form': form})


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, post_id=post_id)
    
    if request.user == comment.author:
        comment.delete()

    return redirect('post_detail', post_id=post_id)