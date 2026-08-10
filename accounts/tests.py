from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Profile


class ProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('profile_user', password='test-password', email='old@example.com')
        Profile.objects.create(user=self.user)

    def test_profile_update(self):
        self.client.login(username='profile_user', password='test-password')
        response = self.client.post(reverse('accounts:profile_edit'), {
            'email': 'new@example.com',
            'bio': '라이트 로스트를 좋아합니다.',
            'location': '서울',
        })
        self.assertRedirects(response, reverse('accounts:mypage'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'new@example.com')
        self.assertEqual(self.user.profile.location, '서울')
