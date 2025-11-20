"""
CMS URL Configuration
"""
from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    # Public views
    path('', views.homepage, name='homepage'),
    path('pages/<slug:slug>/', views.page_detail, name='page_detail'),
    
    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<uuid:post_id>/comment/', views.post_comment, name='post_comment'),
    
    # News
    path('news/', views.news_list, name='news_list'),
    path('news/<slug:slug>/', views.news_detail, name='news_detail'),
    
    # Events
    path('events/', views.events_list, name='events_list'),
    path('events/<slug:slug>/', views.event_detail, name='event_detail'),
    
    # Archives
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('tag/<slug:slug>/', views.tag_view, name='tag'),
    
    # Actions
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('search/', views.search, name='search'),
    
    # Admin - Pages
    path('admin/pages/', views.admin_pages_list, name='admin_pages_list'),
    path('admin/pages/create/', views.admin_page_create, name='admin_page_create'),
    path('admin/pages/<uuid:pk>/edit/', views.admin_page_edit, name='admin_page_edit'),
    path('admin/pages/<uuid:pk>/delete/', views.admin_page_delete, name='admin_page_delete'),
    
    # Admin - Posts
    path('admin/posts/', views.admin_posts_list, name='admin_posts_list'),
    path('admin/posts/create/', views.admin_post_create, name='admin_post_create'),
    path('admin/posts/<uuid:pk>/edit/', views.admin_post_edit, name='admin_post_edit'),
    path('admin/posts/<uuid:pk>/delete/', views.admin_post_delete, name='admin_post_delete'),
    
    # Admin - Media
    path('admin/media/', views.admin_media_list, name='admin_media_list'),
    
    # Admin - Comments
    path('admin/comments/', views.admin_comments_list, name='admin_comments_list'),
    path('admin/comments/<uuid:pk>/approve/', views.admin_comment_approve, name='admin_comment_approve'),
    path('admin/comments/<uuid:pk>/delete/', views.admin_comment_delete, name='admin_comment_delete'),
]
