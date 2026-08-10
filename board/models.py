from django.conf import settings
from django.db import models
from django.urls import reverse


class Post(models.Model):
    class Category(models.TextChoices):
        BEANS = 'beans', '원두 이야기'
        GEAR = 'gear', '커피 장비'
        RECIPE = 'recipe', '추출 레시피'
        TASTING = 'tasting', '시음 노트'
        CAFE = 'cafe', '카페 탐방'

    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.BEANS)
    tags = models.CharField(max_length=200, blank=True, help_text='쉼표로 구분해 입력하세요.')
    bean_amount = models.CharField(max_length=30, blank=True, verbose_name='원두량')
    water_amount = models.CharField(max_length=30, blank=True, verbose_name='물양')
    water_temperature = models.CharField(max_length=30, blank=True, verbose_name='물 온도')
    brew_time = models.CharField(max_length=30, blank=True, verbose_name='추출 시간')
    brew_tool = models.CharField(max_length=80, blank=True, verbose_name='추출 도구')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    view_count = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='liked_posts'
    )
    bookmarked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name='bookmarked_posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('board:post_detail', kwargs={'pk': self.pk})

    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(',') if tag.strip()]

    @property
    def has_recipe_details(self):
        return any([
            self.bean_amount, self.water_amount, self.water_temperature,
            self.brew_time, self.brew_tool,
        ])


class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to='posts/%Y/%m/')
    alt_text = models.CharField(max_length=150, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.post.title} 이미지 {self.order + 1}'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.author} - {self.content[:20]}'
