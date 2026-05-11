from django.db import migrations, models
from django.conf import settings
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = CKEditor5Field('Content', config_name='extends')
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "News"
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.user.username} on {self.news.title}'
class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='news_gallery/')
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Imagen de Galería"
        verbose_name_plural = "Galería de Imágenes"
        ordering = ['created_at']

    def __str__(self):
        return f"Imagen para {self.news.title}"
