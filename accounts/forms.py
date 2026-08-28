from django import forms

from board.forms import validate_image_file
from .models import Profile


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='이메일')

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'location']
        labels = {'avatar': '프로필 이미지', 'bio': '소개', 'location': '활동 지역'}
        widgets = {'bio': forms.Textarea(attrs={'rows': 3})}

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if user:
            self.fields['email'].initial = user.email

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and hasattr(avatar, 'content_type'):
            validate_image_file(avatar)
        return avatar

    def save(self, commit=True):
        profile = super().save(commit=False)
        if self.user:
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save(update_fields=['email'])
        if commit:
            profile.save()
        return profile
