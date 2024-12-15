from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    url = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name ="Category"
        verbose_name_plural = "Categories"
    
    
class Tags(models.Model):
    name = models.CharField(max_length=50)
    url = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name ="Tag"
        verbose_name_plural = "Tags"
    


class Post(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to="blogimages")
    url = models.SlugField(unique=True)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='post')
    tags = models.ManyToManyField(Tags)
    published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name ="Post"
        verbose_name_plural = "Posts"
        
        
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Comment by {self.name} on {self.post.title}'
    
    class Meta:
        verbose_name ="Comment"
        verbose_name_plural = "Comments"
    