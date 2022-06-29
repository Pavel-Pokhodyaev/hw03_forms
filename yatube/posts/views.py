# posts/views.py
from re import template
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from .models import Post, Group, User
from django.contrib.auth import get_user_model
from .forms import PostForm

User = get_user_model()

def index(request):
    posts = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    title = 'Последние обновления на сайте'
    page_obj = paginator.get_page(page_number)
    template = 'posts/index.html'
    context = {
        'title': title,
        'page_obj': page_obj,}
    return render(request, template, context)

@login_required
# Страница с группой
def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = 'Записи сообщества'
    context = {
        'title': title,
        'group': group,
        'posts': posts,
        'page_obj': page_obj,}
    return render(request, 'posts/group_list.html', context)

@login_required
def profile(request, username):
    # Здесь код запроса к модели и создание словаря контекста
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author)
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    template = 'posts/profile.html'
    context = {
        'page_obj' : page_obj,
        'author' : author,
        }
    return render(request, template, context)

@login_required
def post_detail(request, post_id):
    # Здесь код запроса к модели и создание словаря контекста
    post = get_object_or_404(Post, pk=post_id)
    group = post.group
    author = post.author
    context = {
        'author' : author,
        'post' : post,
        'group' : group,
    }
    return render(request, 'posts/post_detail.html', context)

@login_required
def post_create(request):
    """Вью-функция страницы создания публикации"""
    form = PostForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()

        return redirect('posts:profile', username=post.author)

    form = PostForm()

    return render(request, 'posts/create_post.html', {'form': form})

@login_required
def post_edit(request, post_id):
    """Вью-функция изменения публикации"""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(request.POST, instance=post)
    if request.method == 'POST' and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        form.save()

        return redirect('posts:post_detail', post_id=post_id)

    form = PostForm(instance=post)

    return render(
        request,
        'posts/create_post.html',
        {'is_edit': True, 'form': form, 'post': post},
    )
