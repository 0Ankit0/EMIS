"""
Comprehensive CMS Views
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q, Count, F
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from datetime import timedelta

from .models import (
    Page, Post, Category, Tag, Media, Comment,
    Menu, MenuItem, Slider, Widget, Newsletter, SEO
)
from .forms import (
    PageForm, PostForm, CategoryForm, TagForm, MediaForm,
    CommentForm, MenuForm, MenuItemForm, SliderForm,
    WidgetForm, NewsletterForm, SEOForm
)


# ============================================================================
# Public Views
# ============================================================================

def homepage(request):
    """Homepage view"""
    # Get homepage
    homepage = Page.objects.filter(is_homepage=True, status='published').first()
    
    # Featured posts
    featured_posts = Post.objects.filter(
        status='published',
        is_featured=True
    ).order_by('-published_at')[:6]
    
    # Latest news
    latest_news = Post.objects.filter(
        status='published',
        post_type='news'
    ).order_by('-published_at')[:5]
    
    # Upcoming events
    upcoming_events = Post.objects.filter(
        status='published',
        post_type='event',
        event_date__gte=timezone.now()
    ).order_by('event_date')[:5]
    
    # Sliders
    sliders = Slider.objects.filter(is_active=True)
    
    # Apply date filters
    now = timezone.now()
    sliders = sliders.filter(
        Q(start_date__isnull=True) | Q(start_date__lte=now),
        Q(end_date__isnull=True) | Q(end_date__gte=now)
    ).order_by('order')
    
    context = {
        'homepage': homepage,
        'featured_posts': featured_posts,
        'latest_news': latest_news,
        'upcoming_events': upcoming_events,
        'sliders': sliders,
    }
    
    return render(request, 'cms/homepage.html', context)


def page_detail(request, slug):
    """Page detail view"""
    page = get_object_or_404(Page, slug=slug, status='published')
    
    # Increment view count
    Page.objects.filter(pk=page.pk).update(view_count=F('view_count') + 1)
    
    # Get children pages
    children = page.children.filter(status='published').order_by('order')
    
    context = {
        'page': page,
        'children': children,
    }
    
    return render(request, f'cms/pages/{page.template}.html', context)


def blog_list(request):
    """Blog listing view"""
    posts = Post.objects.filter(
        status='published',
        post_type='post'
    ).select_related('author', 'category').prefetch_related('tags')
    
    # Filters
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    search = request.GET.get('q')
    
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    
    if search:
        posts = posts.filter(
            Q(title__icontains=search) |
            Q(content__icontains=search) |
            Q(excerpt__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Sidebar data
    recent_posts = Post.objects.filter(
        status='published',
        post_type='post'
    ).order_by('-published_at')[:5]
    
    popular_posts = Post.objects.filter(
        status='published',
        post_type='post'
    ).order_by('-view_count')[:5]
    
    categories = Category.objects.annotate(
        post_count=Count('posts')
    ).filter(post_count__gt=0)
    
    tags = Tag.objects.annotate(
        post_count=Count('posts')
    ).filter(post_count__gt=0)[:20]
    
    context = {
        'page_obj': page_obj,
        'recent_posts': recent_posts,
        'popular_posts': popular_posts,
        'categories': categories,
        'tags': tags,
    }
    
    return render(request, 'cms/blog/list.html', context)


def post_detail(request, slug):
    """Blog post detail view"""
    post = get_object_or_404(
        Post,
        slug=slug,
        status='published',
        post_type='post'
    )
    
    # Increment view count
    Post.objects.filter(pk=post.pk).update(view_count=F('view_count') + 1)
    
    # Get approved comments
    comments = post.comments.filter(
        status='approved',
        parent__isnull=True
    ).select_related('author').prefetch_related('replies')
    
    # Related posts
    related_posts = Post.objects.filter(
        status='published',
        post_type='post'
    ).exclude(pk=post.pk)
    
    if post.category:
        related_posts = related_posts.filter(category=post.category)
    
    related_posts = related_posts.order_by('-published_at')[:4]
    
    # Previous and next posts
    prev_post = Post.objects.filter(
        status='published',
        post_type='post',
        published_at__lt=post.published_at
    ).order_by('-published_at').first()
    
    next_post = Post.objects.filter(
        status='published',
        post_type='post',
        published_at__gt=post.published_at
    ).order_by('published_at').first()
    
    context = {
        'post': post,
        'comments': comments,
        'related_posts': related_posts,
        'prev_post': prev_post,
        'next_post': next_post,
    }
    
    return render(request, 'cms/blog/detail.html', context)


@csrf_protect
@require_http_methods(["POST"])
def post_comment(request, post_id):
    """Submit a comment"""
    post = get_object_or_404(Post, pk=post_id, allow_comments=True)
    
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        
        if request.user.is_authenticated:
            comment.author = request.user
            comment.author_name = request.user.get_full_name() or request.user.username
            comment.author_email = request.user.email
            comment.status = 'approved'  # Auto-approve for authenticated users
        else:
            # Get client IP
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                comment.author_ip = x_forwarded_for.split(',')[0]
            else:
                comment.author_ip = request.META.get('REMOTE_ADDR')
        
        comment.save()
        
        # Update comment count
        post.comment_count = post.comments.filter(status='approved').count()
        post.save(update_fields=['comment_count'])
        
        messages.success(request, 'Your comment has been submitted successfully!')
    else:
        messages.error(request, 'There was an error with your comment. Please try again.')
    
    return redirect('cms:post_detail', slug=post.slug)


def news_list(request):
    """News listing view"""
    news = Post.objects.filter(
        status='published',
        post_type='news'
    ).order_by('-published_at')
    
    # Pagination
    paginator = Paginator(news, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'cms/news/list.html', context)


def news_detail(request, slug):
    """News detail view"""
    news = get_object_or_404(
        Post,
        slug=slug,
        status='published',
        post_type='news'
    )
    
    # Increment view count
    Post.objects.filter(pk=news.pk).update(view_count=F('view_count') + 1)
    
    # Related news
    related_news = Post.objects.filter(
        status='published',
        post_type='news'
    ).exclude(pk=news.pk).order_by('-published_at')[:5]
    
    context = {
        'news': news,
        'related_news': related_news,
    }
    
    return render(request, 'cms/news/detail.html', context)


def events_list(request):
    """Events listing view"""
    # Upcoming events
    upcoming_events = Post.objects.filter(
        status='published',
        post_type='event',
        event_date__gte=timezone.now()
    ).order_by('event_date')
    
    # Past events
    past_events = Post.objects.filter(
        status='published',
        post_type='event',
        event_date__lt=timezone.now()
    ).order_by('-event_date')
    
    context = {
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    
    return render(request, 'cms/events/list.html', context)


def event_detail(request, slug):
    """Event detail view"""
    event = get_object_or_404(
        Post,
        slug=slug,
        status='published',
        post_type='event'
    )
    
    # Increment view count
    Post.objects.filter(pk=event.pk).update(view_count=F('view_count') + 1)
    
    context = {
        'event': event,
    }
    
    return render(request, 'cms/events/detail.html', context)


def category_view(request, slug):
    """Category archive view"""
    category = get_object_or_404(Category, slug=slug, is_active=True)
    
    posts = Post.objects.filter(
        status='published',
        category=category
    ).order_by('-published_at')
    
    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    
    return render(request, 'cms/category.html', context)


def tag_view(request, slug):
    """Tag archive view"""
    tag = get_object_or_404(Tag, slug=slug)
    
    posts = Post.objects.filter(
        status='published',
        tags=tag
    ).order_by('-published_at')
    
    # Pagination
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    
    return render(request, 'cms/tag.html', context)


@csrf_protect
@require_http_methods(["POST"])
def newsletter_subscribe(request):
    """Newsletter subscription"""
    email = request.POST.get('email', '').strip()
    
    if not email:
        return JsonResponse({'success': False, 'message': 'Email is required'})
    
    # Check if already subscribed
    if Newsletter.objects.filter(email=email, status='active').exists():
        return JsonResponse({
            'success': False,
            'message': 'You are already subscribed to our newsletter'
        })
    
    # Get client IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')
    
    # Create or update subscription
    Newsletter.objects.update_or_create(
        email=email,
        defaults={
            'status': 'active',
            'ip_address': ip_address,
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
        }
    )
    
    return JsonResponse({
        'success': True,
        'message': 'Thank you for subscribing to our newsletter!'
    })


def search(request):
    """Global search"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return render(request, 'cms/search.html', {'query': query})
    
    # Search pages
    pages = Page.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query),
        status='published'
    )[:5]
    
    # Search posts
    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(content__icontains=query),
        status='published'
    )[:10]
    
    context = {
        'query': query,
        'pages': pages,
        'posts': posts,
    }
    
    return render(request, 'cms/search.html', context)


# ============================================================================
# Admin Views
# ============================================================================

@login_required
@permission_required('cms.view_page', raise_exception=True)
def admin_pages_list(request):
    """Admin: Pages list"""
    pages = Page.objects.all().select_related('author').order_by('-created_at')
    
    # Filters
    status = request.GET.get('status')
    if status:
        pages = pages.filter(status=status)
    
    context = {
        'pages': pages,
    }
    
    return render(request, 'cms/admin/pages/list.html', context)


@login_required
@permission_required('cms.add_page', raise_exception=True)
@csrf_protect
def admin_page_create(request):
    """Admin: Create page"""
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            page = form.save(commit=False)
            page.author = request.user
            page.save()
            form.save_m2m()
            
            messages.success(request, f'Page "{page.title}" created successfully!')
            return redirect('cms:admin_pages_list')
    else:
        form = PageForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    
    return render(request, 'cms/admin/pages/form.html', context)


@login_required
@permission_required('cms.change_page', raise_exception=True)
@csrf_protect
def admin_page_edit(request, pk):
    """Admin: Edit page"""
    page = get_object_or_404(Page, pk=pk)
    
    if request.method == 'POST':
        form = PageForm(request.POST, request.FILES, instance=page)
        if form.is_valid():
            page = form.save(commit=False)
            page.updated_by = request.user
            page.save()
            form.save_m2m()
            
            messages.success(request, f'Page "{page.title}" updated successfully!')
            return redirect('cms:admin_pages_list')
    else:
        form = PageForm(instance=page)
    
    context = {
        'form': form,
        'page': page,
        'action': 'Edit',
    }
    
    return render(request, 'cms/admin/pages/form.html', context)


@login_required
@permission_required('cms.delete_page', raise_exception=True)
@require_http_methods(["POST"])
def admin_page_delete(request, pk):
    """Admin: Delete page"""
    page = get_object_or_404(Page, pk=pk)
    title = page.title
    page.delete()
    
    messages.success(request, f'Page "{title}" deleted successfully!')
    return redirect('cms:admin_pages_list')


@login_required
@permission_required('cms.view_post', raise_exception=True)
def admin_posts_list(request):
    """Admin: Posts list"""
    posts = Post.objects.all().select_related('author', 'category').order_by('-created_at')
    
    # Filters
    status = request.GET.get('status')
    post_type = request.GET.get('type')
    
    if status:
        posts = posts.filter(status=status)
    if post_type:
        posts = posts.filter(post_type=post_type)
    
    context = {
        'posts': posts,
    }
    
    return render(request, 'cms/admin/posts/list.html', context)


@login_required
@permission_required('cms.add_post', raise_exception=True)
@csrf_protect
def admin_post_create(request):
    """Admin: Create post"""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            
            messages.success(request, f'Post "{post.title}" created successfully!')
            return redirect('cms:admin_posts_list')
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    
    return render(request, 'cms/admin/posts/form.html', context)


@login_required
@permission_required('cms.change_post', raise_exception=True)
@csrf_protect
def admin_post_edit(request, pk):
    """Admin: Edit post"""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_by = request.user
            post.save()
            form.save_m2m()
            
            messages.success(request, f'Post "{post.title}" updated successfully!')
            return redirect('cms:admin_posts_list')
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
        'action': 'Edit',
    }
    
    return render(request, 'cms/admin/posts/form.html', context)


@login_required
@permission_required('cms.delete_post', raise_exception=True)
@require_http_methods(["POST"])
def admin_post_delete(request, pk):
    """Admin: Delete post"""
    post = get_object_or_404(Post, pk=pk)
    title = post.title
    post.delete()
    
    messages.success(request, f'Post "{title}" deleted successfully!')
    return redirect('cms:admin_posts_list')


@login_required
@permission_required('cms.view_media', raise_exception=True)
def admin_media_list(request):
    """Admin: Media library"""
    media = Media.objects.all().order_by('-uploaded_at')
    
    # Filters
    file_type = request.GET.get('type')
    if file_type:
        media = media.filter(file_type=file_type)
    
    # Pagination
    paginator = Paginator(media, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'cms/admin/media/list.html', context)


@login_required
@permission_required('cms.view_comment', raise_exception=True)
def admin_comments_list(request):
    """Admin: Comments list"""
    comments = Comment.objects.all().select_related('post', 'author').order_by('-created_at')
    
    # Filters
    status = request.GET.get('status')
    if status:
        comments = comments.filter(status=status)
    
    # Pagination
    paginator = Paginator(comments, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    
    return render(request, 'cms/admin/comments/list.html', context)


@login_required
@permission_required('cms.change_comment', raise_exception=True)
@require_http_methods(["POST"])
def admin_comment_approve(request, pk):
    """Admin: Approve comment"""
    comment = get_object_or_404(Comment, pk=pk)
    comment.status = 'approved'
    comment.save()
    
    # Update comment count
    comment.post.comment_count = comment.post.comments.filter(status='approved').count()
    comment.post.save(update_fields=['comment_count'])
    
    messages.success(request, 'Comment approved successfully!')
    return redirect('cms:admin_comments_list')


@login_required
@permission_required('cms.delete_comment', raise_exception=True)
@require_http_methods(["POST"])
def admin_comment_delete(request, pk):
    """Admin: Delete comment"""
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    comment.delete()
    
    # Update comment count
    post.comment_count = post.comments.filter(status='approved').count()
    post.save(update_fields=['comment_count'])
    
    messages.success(request, 'Comment deleted successfully!')
    return redirect('cms:admin_comments_list')
