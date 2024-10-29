from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Blog(models.Model):
    title = models.CharField(verbose_name='Title', max_length=100)
    content = models.TextField(verbose_name='Content')
    posted_at = models.DateTimeField(verbose_name='Posted at', auto_now_add=True)

    class Meta:
        verbose_name_plural = "this is Blog"

    def __str__(self):
         return self.title    
    
class Category(models.Model):
    '''Category'''
    title = models.CharField(
        verbose_name="Category", 
        max_length=20)
    
    def __str__(self):
        return self.title

class Post(models.Model):
    '''post'''
    user = models.ForeignKey(
        CustomUser,
        verbose_name="User",
        on_delete=models.CASCADE)
    
    category = models.ForeignKey(
        Category,
        verbose_name="Category",
        on_delete=models.PROTECT)
    
    title = models.CharField(
        verbose_name="Title",
        max_length=50)
    
    content = models.CharField(verbose_name="Content", max_length=1000)
    
    image1 = models.ImageField(
        verbose_name="image1",
        upload_to="product")
    
    image2 = models.ImageField(
        verbose_name="image2",
        upload_to="product",
        blank=True,
        null=True)

    posted_at = models.DateTimeField(verbose_name="Posted at", auto_now_add=True)

    def __str__(self):
        return self.title
