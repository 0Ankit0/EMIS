"""CMS API URLs"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import (
    CategoryViewSet, TagViewSet, PageViewSet, PostViewSet,
    MediaViewSet, CommentViewSet, MenuViewSet, MenuItemViewSet,
    SliderViewSet, WidgetViewSet, NewsletterViewSet, SEOViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'pages', PageViewSet, basename='page')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'media', MediaViewSet, basename='media')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'menus', MenuViewSet, basename='menu')
router.register(r'menu-items', MenuItemViewSet, basename='menu-item')
router.register(r'sliders', SliderViewSet, basename='slider')
router.register(r'widgets', WidgetViewSet, basename='widget')
router.register(r'newsletter', NewsletterViewSet, basename='newsletter')
router.register(r'seo', SEOViewSet, basename='seo')

urlpatterns = [
    path('', include(router.urls)),
]
