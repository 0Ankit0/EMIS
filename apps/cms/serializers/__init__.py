"""CMS Serializers"""
from .category import CategorySerializer
from .tag import TagSerializer
from .page import PageSerializer, PageListSerializer
from .post import PostSerializer, PostListSerializer
from .media import MediaSerializer
from .comment import CommentSerializer
from .menu import MenuSerializer, MenuItemSerializer
from .slider_widget import SliderSerializer, WidgetSerializer
from .newsletter_seo import NewsletterSerializer, SEOSerializer

__all__ = [
    'CategorySerializer',
    'TagSerializer',
    'PageSerializer',
    'PageListSerializer',
    'PostSerializer',
    'PostListSerializer',
    'MediaSerializer',
    'CommentSerializer',
    'MenuSerializer',
    'MenuItemSerializer',
    'SliderSerializer',
    'WidgetSerializer',
    'NewsletterSerializer',
    'SEOSerializer',
]
