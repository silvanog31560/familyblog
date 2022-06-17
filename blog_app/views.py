from django.shortcuts import get_object_or_404, redirect
from blog_app.models import Post, Comment
from blog_app.forms import PostForm, CommentForm
from django.views.generic import TemplateView, DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.utils import timezone


# Create your views here.
class AboutView(TemplateView):
    template_name = 'blog_app/about.html'

class PostListView(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    login_url = '/login/'
    redirect_field_name = 'blog_app/post_detail.html'
    form_class = PostForm

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog_app/post_detail.html'
    model = Post
    form_class = PostForm

@method_decorator(login_required, name='dispatch')
class PostDeleteView(DeleteView):
    login_url = '/login/'
    redirect_field_name = 'blog_app/post_detail.html'
    model = Post
    success_url = reverse_lazy('blog_app:post_list')

@method_decorator(login_required, name='dispatch')
class DraftListView(ListView):
    login_url = '/login/'
    redirect_field_name = 'blog_app/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

class CommentFormView(FormView):
    template_name = 'blog_app/comment_form.html'
    form_class = CommentForm
    success_url = reverse_lazy('blog_app:post_detail/pk')

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        return redirect('blog_app:post_detail', pk=post.pk)


###########################################################################

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog_app:post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog_app:post_detail', pk=post_pk)

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('blog_app:post_detail', pk=pk)
