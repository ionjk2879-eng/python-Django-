from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('accounts:login')


class MyPageView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts/mypage.html'
    context_object_name = 'member'

    def get_object(self, queryset=None):
        return self.request.user
