from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
    ''' Danh mục '''
    title = models.CharField(verbose_name="Danh mục", max_length=20)
    class Meta:
        # tên model biểu thị trong admin
        verbose_name_plural = "Danh mục (Categories)"
    
    def __str__(self):
        return self.title
    
class Post(models.Model):
    ''' Bài viết '''
    user = models.ForeignKey(
        CustomUser,
        verbose_name='User',
        on_delete=models.CASCADE)
    
    category = models.ForeignKey(
        Category, verbose_name='Danh mục',
        on_delete=models.PROTECT)
    
    title = models.CharField(verbose_name='Tên bài post', max_length=100)

    content = models.TextField(verbose_name='Nội dung')

    image1 = models.ImageField(
        verbose_name='Ảnh 1',
        upload_to = 'photos')
    
    image2 = models.ImageField(
        verbose_name="Ảnh 2",
        upload_to= 'photos',
        blank=True,
        null=True) 

    posted_at = models.DateTimeField(verbose_name="ngay-dang-bai", auto_now_add=True)

    def __str__(self):
        return f'{self.title}'
    class Meta:
        # tên model biểu thị trong admin
        verbose_name_plural = "Bài viết (Posts)"
    
class Comment(models.Model):
    ''' Phần bình luận '''
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, verbose_name='User', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Nội dung')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.content[:20]}'
    
    class Meta:
        # tên model biểu thị trong admin
        verbose_name_plural = "Phần bình luận (Comments)"