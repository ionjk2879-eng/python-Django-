import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Post, PostImage


TEMP_MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class BoardFeatureTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)

    def setUp(self):
        self.user = User.objects.create_user('coffee_user', password='test-password')
        self.post = Post.objects.create(
            author=self.user,
            title='에티오피아 원두 기록',
            content='복숭아 향이 좋은 원두입니다.',
            category=Post.Category.BEANS,
            tags='에티오피아, 내추럴',
        )

    def test_category_filter_and_tag_search(self):
        response = self.client.get(reverse('board:community'), {'category': 'beans', 'q': '내추럴'})
        self.assertContains(response, self.post.title)

    def test_image_upload_on_post_create(self):
        self.client.login(username='coffee_user', password='test-password')
        image = SimpleUploadedFile('coffee.png', b'fake-png-content', content_type='image/png')
        response = self.client.post(reverse('board:post_create'), {
            'category': Post.Category.RECIPE,
            'title': '새 레시피',
            'content': '원두 20g, 물 300g',
            'tags': 'V60, 레시피',
            'images': image,
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(PostImage.objects.filter(post__title='새 레시피').count(), 1)

    def test_like_and_bookmark_toggle(self):
        self.client.login(username='coffee_user', password='test-password')
        self.client.post(reverse('board:post_like', args=[self.post.pk]))
        self.client.post(reverse('board:post_bookmark', args=[self.post.pk]))
        self.assertTrue(self.post.liked_by.filter(pk=self.user.pk).exists())
        self.assertTrue(self.post.bookmarked_by.filter(pk=self.user.pk).exists())
        self.client.post(reverse('board:post_like', args=[self.post.pk]))
        self.assertFalse(self.post.liked_by.filter(pk=self.user.pk).exists())

    def test_detail_renders_without_profile(self):
        response = self.client.get(reverse('board:post_detail', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)
