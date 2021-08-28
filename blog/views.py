from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, Comment, Tag
from django.utils import timezone
from .forms import BlogForm, CommentForm
from django.db.models import Q
from django import forms
from django.views.generic import ListView, DetailView, TemplateView

def home(request):
    blogs = Blog.objects.all()
    return render(request, 'home.html', {'blogs':blogs})

def gallery(request):
    blogs = Blog.objects.all()
    return render(request, 'gallery.html', {'blogs':blogs})

def detail(request, id):
    blog = get_object_or_404(Blog, pk=id)
    comments = Comment.objects.filter(post_id=id, comment_id__isnull=True)

    re_comments = []
    for comment in comments:
        re_comments += list(Comment.objects.filter(comment_id=comment.id))
    
    form = CommentForm()
    return render(request, 'detail.html', {'blog':blog, 'comments':comments, 're_comments':re_comments, 'form':form})


def delete(request, id):
    delete_blog = Blog.objects.get(id=id)
    delete_blog.delete()
    return redirect('gallery')


def new(request):
    if request.method == 'POST':
        blog_form = BlogForm(request.POST, request.FILES)
        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.pub_date = timezone.now()
            blog.save()

            tags = blog_form.cleaned_data['tag'].split(',')
            for tag in tags:
                if not tag : 
                    continue
                else:
                    tag = tag.strip()
                    tag_, created = Tag.objects.get_or_create(name = tag)
                    blog.tag.add(tag_)
            
            return redirect('gallery')
    else:
        blog_form = BlogForm()
        return render(request, 'new.html', {'blog_form':blog_form})

def edit(request, id):
    blog = get_object_or_404(Blog, pk=id)
    if request.method == 'GET':
        blog_form = BlogForm(instance=blog)
        return render(request, 'edit.html', {'edit_blog':blog_form})
    else:
        blog_form = BlogForm(request.POST, request.FILES, instance=blog)
        if blog_form.is_valid():
            blog = blog_form.save(commit=False)
            blog.pub_date = timezone.now()
            blog.save()
        return redirect('/blog/' + str(id))

def create_comment(request, article_id):
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post_id = Blog.objects.get(pk=article_id)
            # comment.author = request.user
            comment.created_at = timezone.now()
            comment.save()
    return redirect('detail', article_id)

def create_re_comment(request, article_id, comment_id):
    if request.method == 'POST':
        comment_form= CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post_id = Blog.objects.get(pk=article_id)
            comment.comment_id = Comment.objects.get(pk=comment_id)
            # comment.author = request.user
            comment.created_at = timezone.now()
            comment.save()
    return redirect('detail', article_id)

def delete_comment(request, comment_id, article_id):
    mycom = Comment.objects.get(id=comment_id)
    mycom.delete()
    return redirect('detail', article_id)

def search(request):
    keyword = request.POST.get('keyword', '')
    type = request.POST.get('type', '')
    searched_posts = Blog.objects.order_by('-id')

    if keyword :
        if type == 'title':
            searched_posts = searched_posts.filter(title__icontains=keyword)
        elif type == 'body':
            searched_posts = searched_posts.filter(body__icontains=keyword)
        return render(request, 'search.html', {'searched':keyword, 'searched_posts': searched_posts})
    else:
         return render(request, 'search.html')