"""
CMS Forms
"""
from django import forms
from .models import (
    Page, Post, Category, Tag, Media, Comment,
    Menu, MenuItem, Slider, Widget, Newsletter, SEO
)


class PageForm(forms.ModelForm):
    """Page form"""
    class Meta:
        model = Page
        fields = [
            'title', 'slug', 'content', 'excerpt',
            'meta_title', 'meta_description', 'meta_keywords',
            'featured_image', 'parent', 'template', 'order',
            'status', 'is_homepage', 'show_in_menu'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'Page Title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'page-slug'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'rows': 15,
                'id': 'editor'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'rows': 3
            }),
            'meta_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'rows': 3
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'parent': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'template': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
        }


class PostForm(forms.ModelForm):
    """Post form"""
    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'content', 'excerpt', 'post_type',
            'category', 'tags', 'featured_image',
            'meta_title', 'meta_description', 'meta_keywords',
            'status', 'is_featured', 'is_pinned', 'allow_comments',
            'scheduled_for', 'event_date', 'event_end_date', 'event_location'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'Post Title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'post-slug'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'rows': 15,
                'id': 'editor'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'rows': 3
            }),
            'post_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'size': '5'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'scheduled_for': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'type': 'datetime-local'
            }),
            'event_date': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'type': 'datetime-local'
            }),
            'event_end_date': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'type': 'datetime-local'
            }),
            'event_location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
        }


class CategoryForm(forms.ModelForm):
    """Category form"""
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'parent', 'icon', 'color', 'order', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'rows': 3
            }),
            'parent': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'fa-icon-name'
            }),
            'color': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'type': 'color'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
        }


class TagForm(forms.ModelForm):
    """Tag form"""
    class Meta:
        model = Tag
        fields = ['name', 'slug', 'description', 'color']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'rows': 3
            }),
            'color': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'type': 'color'
            }),
        }


class MediaForm(forms.ModelForm):
    """Media upload form"""
    class Meta:
        model = Media
        fields = ['title', 'file', 'alt_text', 'caption', 'description', 'folder', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'file': forms.FileInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'alt_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'caption': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'rows': 2
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'rows': 3
            }),
            'folder': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
        }


class CommentForm(forms.ModelForm):
    """Comment form"""
    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'content', 'parent']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'Your Name',
                'required': True
            }),
            'author_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'your@email.com',
                'required': True
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'rows': 4,
                'placeholder': 'Your comment...',
                'required': True
            }),
            'parent': forms.HiddenInput(),
        }


class MenuForm(forms.ModelForm):
    """Menu form"""
    class Meta:
        model = Menu
        fields = ['name', 'location', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'location': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'rows': 3
            }),
        }


class MenuItemForm(forms.ModelForm):
    """Menu item form"""
    class Meta:
        model = MenuItem
        fields = [
            'menu', 'title', 'link_type', 'page', 'post', 'category',
            'custom_url', 'icon', 'css_class', 'target', 'parent', 'order', 'is_active'
        ]
        widgets = {
            'menu': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'link_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'page': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'post': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'custom_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'css_class': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'target': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'parent': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
        }


class SliderForm(forms.ModelForm):
    """Slider form"""
    class Meta:
        model = Slider
        fields = [
            'title', 'description', 'image', 'mobile_image',
            'link_text', 'link_url', 'order', 'is_active',
            'start_date', 'end_date'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'rows': 3
            }),
            'link_text': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'link_url': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'type': 'datetime-local'
            }),
        }


class WidgetForm(forms.ModelForm):
    """Widget form"""
    class Meta:
        model = Widget
        fields = [
            'title', 'widget_type', 'position', 'content', 'settings',
            'order', 'is_active', 'show_on_pages', 'show_on_posts'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'widget_type': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'position': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'rows': 10
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'show_on_pages': forms.SelectMultiple(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
        }


class NewsletterForm(forms.ModelForm):
    """Newsletter subscription form"""
    class Meta:
        model = Newsletter
        fields = ['email', 'name']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'your@email.com',
                'required': True
            }),
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'placeholder': 'Your Name (Optional)'
            }),
        }


class SEOForm(forms.ModelForm):
    """SEO form"""
    class Meta:
        model = SEO
        fields = [
            'title', 'description', 'keywords',
            'og_title', 'og_description', 'og_image',
            'twitter_title', 'twitter_description', 'twitter_image',
            'schema_type', 'schema_data', 'index', 'follow', 'canonical_url'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'rows': 3
            }),
            'keywords': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'og_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'og_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'rows': 2
            }),
            'twitter_title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'twitter_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg',
                'rows': 2
            }),
            'schema_type': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
            'canonical_url': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border rounded-lg'
            }),
        }
