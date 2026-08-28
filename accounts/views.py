from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from .forms import ProfileForm
from .models import Profile


class MyPageView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/mypage.html'
    context_object_name = 'member'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'], _ = Profile.objects.get_or_create(user=self.request.user)
        context['posts'] = self.request.user.posts.prefetch_related('images').all()
        context['bookmarks'] = self.request.user.bookmarked_posts.prefetch_related('images')[:4]
        context['post_count'] = self.request.user.posts.count()
        context['comment_count'] = self.request.user.comments.count()
        context['bookmark_count'] = self.request.user.bookmarked_posts.count()
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'accounts/profile_form.html'
    success_url = reverse_lazy('accounts:mypage')

    def get_object(self, queryset=None):
        profile, _ = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
