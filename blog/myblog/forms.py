from django import forms
from django.forms import ModelForm
from .models import Post, Comment

class ContactForm(forms.Form):
    name = forms.CharField(label='Họ và tên')
    email = forms.EmailField(label='Email')
    phonenumber = forms.CharField(label='Số điện thoại')
    message = forms.CharField(label='Lời nhắn', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        '''Constructor of ContactForm
        
        Khởi tạo các trường dữ liệu(field)
        '''
        super().__init__(*args, **kwargs)

        # tạo lời nhắn ở placeholder của field name
        self.fields['name'].widget.attrs['placeholder'] = \
        'Hãy nhập họ và tên của bạn'

        # thiết lập thuộc tính class của thẻ <input> mà sẽ xuất field name
        self.fields['name'].widget.attrs['class'] = 'form-control'
        
        # tạo lời nhắn ở placeholder của field email
        self.fields['email'].widget.attrs['placeholder'] = \
        'Hãy nhập email của bạn'
        # thiết lập thuộc tính class của thẻ <input> mà sẽ xuất field email
        self.fields['email'].widget.attrs['class'] = 'form-control'

        # tạo lời nhắn ở placeholder của field phonenumber
        self.fields['phonenumber'].widget.attrs['placeholder'] = \
        'Hãy nhập số điện thoại'
        # thiết lập thuộc tính class của thẻ <input> mà sẽ xuất field phonenumber
        self.fields['phonenumber'].widget.attrs['class'] = 'form-control'

        # tạo lời nhắn ở placeholder của field message
        self.fields['message'].widget.attrs['placeholder'] = \
        'Hãy nhập lời nhắn của bạn'
        # thiết lập thuộc tính class của thẻ <input> mà sẽ xuất field message
        self.fields['message'].widget.attrs['class'] = 'form-control'

        
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'image1', 'image2']
        


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control custom-content',  # Thêm class CSS tùy chỉnh
                'placeholder': 'Viết bình luận của bạn...',
                'rows': 3,
                'style': 'resize: none;',  # Tùy chọn style CSS, nếu muốn
            }),
        }
        