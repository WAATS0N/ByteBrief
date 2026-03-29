from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, blank=True, null=True)
    rss_url = models.URLField(max_length=500, blank=True, null=True)
    base_url = models.URLField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=500)
    summary = models.TextField()
    content = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    url = models.URLField(max_length=1000, unique=True)
    image_url = models.URLField(max_length=1000, blank=True, null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='articles')
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    categories = models.JSONField(default=list, help_text="List of preferred categories")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Preferences"

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'article')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} bookmarked {self.article.title}"
