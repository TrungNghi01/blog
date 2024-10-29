from django import forms
from django.forms import ModelForm
from .models import Post

class ContactForm(forms.Form):
    name = forms.CharField(label = "Full name")
    email = forms.EmailField(label="Email")
    phoneNumber = forms.CharField(label="Phone number")
    message = forms.CharField(label="Message", widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add placeholders and classes to form fields
        self.fields['name'].widget.attrs['placeholder'] = \
        'Enter your full name'
        # Add class to form field
        self.fields['name'].widget.attrs['class'] = 'form-control'

        self.fields['email'].widget.attrs['placeholder'] = \
        'Enter your email address'
        self.fields['email'].widget.attrs['class'] = 'form-control'

        self.fields['phoneNumber'].widget.attrs['placeholder'] = \
        'Enter your phone number'
        self.fields['phoneNumber'].widget.attrs['class'] = 'form-control'

        self.fields['message'].widget.attrs['placeholder'] = \
        'Enter your message here'
        self.fields['message'].widget.attrs['class'] = 'form-control'


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'image1', 'image2']
        # labels = {
        #     'category': 'Category',
        #     'title': 'Title',
        #     'content': 'Content',
        #     'image1': 'Image 1',
        #     'image2': 'Image 2'
        # }
        # widgets = {
        #     'category': forms.Select(attrs={'class': 'form-control'}),
        #     'title': forms.TextInput(attrs={'class': 'form-control'}),
        #     'content': forms.Textarea(attrs={'class': 'form-control'}),
        #     'image1': forms.FileInput(attrs={'class': 'form-control'}),
        #     'image2': forms.FileInput(attrs={'class': 'form-control'})
        # }

    