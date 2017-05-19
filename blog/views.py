from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import PostForm
from django.utils import timezone


def post_list(request):
    published_posts = Post.objects\
        .filter(published_date__lte=timezone.now())\
        .order_by("published_date")\
        .reverse()
    return render(request, "blog/post_list.html", {"posts": published_posts})


def post_detail(request, pk):
    valid_post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": valid_post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post_to_save = form.save(commit=False)
            post_to_save.author = request.user
            post_to_save.published_date = timezone.now()
            post_to_save.save()
            return redirect('post_detail', pk=post_to_save.pk)
    else:
        form = PostForm()
    return render(request, "blog/post_edit.html", {'form': form, 'header': 'New Post'})

"""
### Gammel version af metoden: I stedet for DG-tilgangen,
### traekker den oplysninger ud af formen og gemmer dem
### direkte i database-modellen

def post_edit(request, pk):
    #post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post_to_resave = Post.objects.get(pk=pk)
            post_to_resave.title = form.cleaned_data['title']
            post_to_resave.text = form.cleaned_data['text']
            post_to_resave.save()
            return redirect('post_detail', pk=pk)
    # else:
    post_object = Post.objects.get(pk=pk)
    form = PostForm(instance=post_object)
    return render(request, "blog/post_edit.html", {'form': form})
"""

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {'form': form, 'header': 'Edit Post'})