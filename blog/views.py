from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment
from .forms import CommentForm
from django.db.models import Q


# def home(request):
#     context = {"posts": Post.objects.all()}
#     return render(request, "blog/home.html", context)


def budget(request):
    return render(request, "blog/budget.html")


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"  # <app>/<model>_<viewtype>.html
    context_object_name = "posts"
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = "blog/user_posts.html"  # <app>/<model>_<viewtype>.html
    context_object_name = "posts"
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Post.objects.filter(author=user).order_by("-date_posted")


class PostDetailView(DetailView):
    model = Post
    # <app>/<model>_<viewtype>.html

    def get_object(self):
        obj = super().get_object()
        obj.blog_views += 1
        obj.save()
        return obj


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content", "image"]

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        # post.image = form.cleaned_data['image']
        post.save()
        return redirect('blog-home')


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content", 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post-detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post-detail', pk=comment.post.pk)


def upvote_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.update_upvote()
    print(post.get_upvotes)
    return redirect('post-detail', pk=post.pk)


def downvote_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.update_downvote()
    return redirect('post-detail', pk=post.pk)


def search_posts(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        if query is not None:
            lookups = Q(title__icontains=query) | Q(content__icontains=query) | Q(author__username__icontains=query)
            results = Post.objects.filter(lookups).distinct()
            return render(request, 'blog/search.html', {'results': results})
        else:
            return render(request, 'blog/search.html')

    else:
        return render(request, 'blog/search.html')


def about(request):
    return render(request, "blog/about.html", {"title": "About"})
