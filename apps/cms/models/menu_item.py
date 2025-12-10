import uuid
from django.db import models
from .menu import Menu
from .page import Page
from .post import Post
from .category import Category

class MenuItem(models.Model):
    """Menu items"""
    LINK_TYPES = [
        ('page', 'Page'),
        ('post', 'Post'),
        ('category', 'Category'),
        ('custom', 'Custom URL'),
        ('external', 'External URL'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200)
    link_type = models.CharField(max_length=20, choices=LINK_TYPES)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    custom_url = models.CharField(max_length=500, blank=True)
    icon = models.CharField(max_length=50, blank=True)
    css_class = models.CharField(max_length=100, blank=True)
    target = models.CharField(
        max_length=20,
        choices=[('_self', 'Same Window'), ('_blank', 'New Window')],
        default='_self'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    class Meta:
        db_table = 'cms_menu_items'
        ordering = ['order']
    def __str__(self):
        return f'{self.menu.name} - {self.title}'
    def get_url(self):
        if self.link_type == 'page' and self.page:
            return f'/pages/{self.page.slug}/'
        elif self.link_type == 'post' and self.post:
            return f'/blog/{self.post.slug}/'
        elif self.link_type == 'category' and self.category:
            return f'/category/{self.category.slug}/'
        elif self.link_type in ['custom', 'external']:
            return self.custom_url
        return '#'
