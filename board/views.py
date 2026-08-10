from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.db import transaction
from django.db.models import Count, F, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CommentForm, PostForm
from .models import Comment, Post, PostImage


class PostListView(ListView):
    model = Post
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if request.resolver_match.url_name == 'post_list' and request.GET:
            community_url = reverse('board:community')
            return redirect(f'{community_url}?{request.GET.urlencode()}')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().select_related('author', 'author__profile').prefetch_related('images').annotate(
            comment_count=Count('comments', distinct=True),
            like_count=Count('liked_by', distinct=True),
        ).order_by('-created_at')
        query = self.request.GET.get('q', '').strip()
        search_type = self.request.GET.get('type', 'all')
        category = self.request.GET.get('category', '').strip()
        if category in Post.Category.values:
            queryset = queryset.filter(category=category)
        if not query:
            return queryset

        if search_type == 'title':
            condition = Q(title__icontains=query)
        elif search_type == 'content':
            condition = Q(content__icontains=query)
        elif search_type == 'author':
            condition = Q(author__username__icontains=query)
        else:
            condition = (
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(author__username__icontains=query)
                | Q(tags__icontains=query)
            )
        return queryset.filter(condition)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_home'] = (
            self.request.resolver_match.url_name == 'post_list'
            and not self.request.GET.get('q')
            and not self.request.GET.get('category')
        )
        context['query'] = self.request.GET.get('q', '')
        context['search_type'] = self.request.GET.get('type', 'all')
        context['selected_category'] = self.request.GET.get('category', '')
        context['categories'] = Post.Category.choices
        return context


class PostDetailView(DetailView):
    model = Post

    def get_queryset(self):
        return super().get_queryset().select_related('author', 'author__profile').prefetch_related('images', 'liked_by', 'bookmarked_by')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Post.objects.filter(pk=obj.pk).update(view_count=F('view_count') + 1)
        obj.refresh_from_db(fields=['view_count'])
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('author', 'author__profile')
        context['comment_form'] = CommentForm()
        context['is_liked'] = self.request.user.is_authenticated and self.object.liked_by.filter(pk=self.request.user.pk).exists()
        context['is_bookmarked'] = self.request.user.is_authenticated and self.object.bookmarked_by.filter(pk=self.request.user.pk).exists()
        return context


class PostImageFormMixin:
    @transaction.atomic
    def form_valid(self, form):
        new_images = form.cleaned_data.get('images', [])
        current_count = self.object.images.count() if getattr(self, 'object', None) else 0
        delete_ids = self.request.POST.getlist('delete_images')
        if delete_ids and getattr(self, 'object', None):
            self.object.images.filter(pk__in=delete_ids).delete()
            current_count = self.object.images.count()
        if current_count + len(new_images) > 5:
            form.add_error('images', '게시글 이미지는 전체 5장까지 저장할 수 있습니다.')
            return self.form_invalid(form)
        response = super().form_valid(form)
        start_order = self.object.images.count()
        for index, image in enumerate(new_images):
            PostImage.objects.create(
                post=self.object,
                image=image,
                alt_text=f'{self.object.title} 첨부 이미지',
                order=start_order + index,
            )
        return response


class PostCreateView(LoginRequiredMixin, PostImageFormMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostAuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class PostUpdateView(LoginRequiredMixin, PostAuthorRequiredMixin, PostImageFormMixin, UpdateView):
    model = Post
    form_class = PostForm


class PostDeleteView(LoginRequiredMixin, PostAuthorRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('board:post_list')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('board:post_detail', kwargs={'pk': self.kwargs['post_pk']})


class CommentAuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author == self.request.user


class CommentUpdateView(LoginRequiredMixin, CommentAuthorRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.is_ajax():
            return JsonResponse({'content': self.object.content})
        return response

    def form_invalid(self, form):
        if self.is_ajax():
            return JsonResponse({'errors': form.errors.get_json_data()}, status=400)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('board:post_detail', kwargs={'pk': self.object.post_id})


class CommentDeleteView(LoginRequiredMixin, CommentAuthorRequiredMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('board:post_detail', kwargs={'pk': self.object.post_id})


class PostReactionView(LoginRequiredMixin, DetailView):
    model = Post
    reaction_field = ''

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        relation = getattr(post, self.reaction_field)
        active = relation.filter(pk=request.user.pk).exists()
        if active:
            relation.remove(request.user)
        else:
            relation.add(request.user)
        count = relation.count()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'active': not active, 'count': count})
        messages.success(request, '저장했습니다.')
        return redirect('board:post_detail', pk=post.pk)


class PostLikeView(PostReactionView):
    reaction_field = 'liked_by'


class PostBookmarkView(PostReactionView):
    reaction_field = 'bookmarked_by'
