from django import forms
from django.core.exceptions import ValidationError

from .models import Image, Tag


class ImageForm(forms.ModelForm):
    images = forms.FileField(widget=forms.TextInput(attrs={
            "name": "images",
            "type": "File",
            "class": "form-control",
            "multiple": "True",
        }), label="")

    class Meta:
        model = Image
        fields = ['images']

    def clean_images(self):
        images = self.cleaned_data.get('images')
        if images:
            if not images.content_type.startswith('image/'):
                raise ValidationError('Only image files are allowed.')
        return images


class TagForm(forms.ModelForm):
    tags = forms.CharField(max_length=200, required=True, help_text="Enter tags separated by commas")

    class Meta:
        model = Tag
        fields = ['tags']
