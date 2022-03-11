from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User, Follow
from django.core.paginator import Paginator
from .forms import CommentForm, PostForm
from django.contrib.auth.decorators import login_required

POST_PER_PAGES = 10


def index(request) -> None:
    posts_list = Post.objects.all()
    template = "posts/index.html"
    paginator = Paginator(posts_list, POST_PER_PAGES)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, template, context)


def group_posts(request, slug) -> None:
    template = "posts/group_list.html"
    group = get_object_or_404(Group, slug=slug)
    paginator = Paginator(group.posts.all(), POST_PER_PAGES)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj, "group": group}
    return render(request, template, context)


def profile(request, username) -> None:
    template = "posts/profile.html"
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author)
    post_count = post_list.count()
    paginator = Paginator(post_list.all(), POST_PER_PAGES)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    if request.user == author:
        owner = 1
    else:
        owner = 0
    following = (
        request.user.is_authenticated and Follow.objects.filter(
            user=request.user, author=author).exists())
    context = {
        "page_obj": page_obj,
        "post_count": post_count,
        "author": author,
        "following": following,
        'owner': owner,
    }
    return render(request, template, context)


def post_detail(request, post_id) -> None:
    template = "posts/post_detail.html"
    post = get_object_or_404(Post, pk=post_id)
    post_list = Post.objects.filter(author=post.author)
    post_count = post_list.count()
    post_comments = post.comments.all()
    form = CommentForm(request.POST or None)
    context = {
        "post": post,
        "post_count": post_count,
        "comments": post_comments,
        "form": form,
    }
    return render(request, template, context)


@login_required
def post_create(request) -> None:
    form = PostForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, "posts/create_post.html", {"form": form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect("posts:profile", username=request.user)


def post_edit(request, post_id) -> None:
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect("posts:post_detail", post_id=post_id)
    is_edit = True
    form = PostForm(
        request.POST or None,
        instance=post,
        files=request.FILES or None,
    )
    if not form.is_valid():
        form = PostForm(instance=post)
        context = {"form": form, "is_edit": is_edit, "post": post}
        return render(request, "posts/create_post.html", context)
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect("posts:post_detail", post_id=post_id)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if not form.is_valid():
        return redirect("posts:post_detail", post_id=post_id)
    comment = form.save(commit=False)
    comment.author = request.user
    comment.post = post
    comment.save()
    return redirect("posts:post_detail", post_id=post_id)


@login_required
def follow_index(request):
    followers = list(Follow.objects.filter(user=request.user))
    authors = []
    for follower in followers:
        authors.append(follower.author)
    posts_list = Post.objects.filter(author__in=authors)
    template = "posts/follow.html"
    paginator = Paginator(posts_list, POST_PER_PAGES)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    test_follow = Follow.objects.filter(
        user=request.user,
        author=author,
    ).exists()
    if author != request.user and test_follow == 0:
        Follow.objects.create(
            user=request.user,
            author=author,
        )
    return redirect("posts:profile", username=username)


@login_required
def profile_unfollow(request, username):
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(
        user=request.user,
        author=author,
    ).delete()
    return redirect("posts:profile", username=username)
