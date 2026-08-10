from pathlib import Path

from django import forms

from .models import Comment, Post


ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp'}
ALLOWED_IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp'}
MAX_IMAGE_SIZE = 5 * 1024 * 1024


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        single_clean = super().clean
        if not data:
            return []
        files = data if isinstance(data, (list, tuple)) else [data]
        return [single_clean(item, initial) for item in files]


def validate_image_file(upload):
    extension = Path(upload.name).suffix.lower()
    content_type = getattr(upload, 'content_type', '')
    if extension not in ALLOWED_IMAGE_EXTENSIONS or content_type not in ALLOWED_IMAGE_TYPES:
        raise forms.ValidationError('JPEG, PNG, WebP 이미지만 업로드할 수 있습니다.')
    if upload.size > MAX_IMAGE_SIZE:
        raise forms.ValidationError('이미지는 파일당 5MB 이하여야 합니다.')
    return upload


class PostForm(forms.ModelForm):
    images = MultipleFileField(required=False, help_text='최대 5장, 파일당 5MB')

    class Meta:
        model = Post
        fields = [
            'category', 'title', 'content', 'tags', 'bean_amount',
            'water_amount', 'water_temperature', 'brew_time', 'brew_tool',
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 12}),
            'tags': forms.TextInput(attrs={'placeholder': '예: 에티오피아, V60, 내추럴'}),
        }

    def clean_images(self):
        images = self.cleaned_data.get('images', [])
        if len(images) > 5:
            raise forms.ValidationError('이미지는 최대 5장까지 업로드할 수 있습니다.')
        for image in images:
            validate_image_file(image)
        return images


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'rows': 2})}
