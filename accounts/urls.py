from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('mypage/', views.MyPageView.as_view(), name='mypage'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
]
