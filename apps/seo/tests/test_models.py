"""SEO Tests"""
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from apps.seo.models import SEOMetadata, Redirect, SitemapConfig, RobotsConfig, SEOAnalytics
from apps.seo.services import SEOService, SitemapService, RobotsService

User = get_user_model()


class SEOMetadataModelTest(TestCase):
    """Test SEO Metadata Model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.content_type = ContentType.objects.get_for_model(User)
    
    def test_create_seo_metadata(self):
        """Test creating SEO metadata"""
        seo = SEOMetadata.objects.create(
            content_type=self.content_type,
            object_id=self.user.pk,
            meta_title='Test Title',
            meta_description='Test Description'
        )
        self.assertEqual(seo.meta_title, 'Test Title')
        self.assertEqual(seo.og_title, 'Test Title')  # Auto-populated
        self.assertEqual(seo.twitter_title, 'Test Title')  # Auto-populated
    
    def test_seo_metadata_unique_together(self):
        """Test unique constraint on content_type and object_id"""
        SEOMetadata.objects.create(
            content_type=self.content_type,
            object_id=self.user.pk,
            meta_title='Test 1',
            meta_description='Desc 1'
        )
        
        with self.assertRaises(Exception):
            SEOMetadata.objects.create(
                content_type=self.content_type,
                object_id=self.user.pk,
                meta_title='Test 2',
                meta_description='Desc 2'
            )


class RedirectModelTest(TestCase):
    """Test Redirect Model"""
    
    def test_create_redirect(self):
        """Test creating a redirect"""
        redirect = Redirect.objects.create(
            old_path='/old-page/',
            new_path='/new-page/',
            redirect_type='301'
        )
        self.assertEqual(redirect.hit_count, 0)
        self.assertTrue(redirect.is_active)
    
    def test_increment_hits(self):
        """Test incrementing hit counter"""
        redirect = Redirect.objects.create(
            old_path='/test/',
            new_path='/new-test/',
            redirect_type='301'
        )
        redirect.increment_hits()
        redirect.refresh_from_db()
        self.assertEqual(redirect.hit_count, 1)
    
    def test_redirect_manager_active(self):
        """Test active manager method"""
        Redirect.objects.create(
            old_path='/active/',
            new_path='/new/',
            redirect_type='301',
            is_active=True
        )
        Redirect.objects.create(
            old_path='/inactive/',
            new_path='/new/',
            redirect_type='301',
            is_active=False
        )
        
        active_redirects = Redirect.objects.active()
        self.assertEqual(active_redirects.count(), 1)


class SitemapConfigModelTest(TestCase):
    """Test Sitemap Config Model"""
    
    def test_create_sitemap_config(self):
        """Test creating sitemap configuration"""
        config = SitemapConfig.objects.create(
            app_label='seo',
            model_name='SEOMetadata',
            priority=0.8,
            changefreq='daily'
        )
        self.assertTrue(config.is_enabled)
        self.assertEqual(config.priority, 0.8)


class RobotsConfigModelTest(TestCase):
    """Test Robots Config Model"""
    
    def test_create_robots_config(self):
        """Test creating robots.txt configuration"""
        config = RobotsConfig.objects.create(
            user_agent='*',
            disallow='/admin/\n/api/private/',
            allow='/api/public/'
        )
        self.assertTrue(config.is_active)
        self.assertIn('/admin/', config.disallow)


class SEOAnalyticsModelTest(TestCase):
    """Test SEO Analytics Model"""
    
    def test_create_analytics(self):
        """Test creating analytics configuration"""
        analytics = SEOAnalytics.objects.create(
            name='Google Analytics',
            platform='ga',
            tracking_id='UA-12345678-1'
        )
        self.assertTrue(analytics.is_active)
        self.assertTrue(analytics.in_head)


class SEOServiceTest(TestCase):
    """Test SEO Service"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='servicetest',
            email='service@example.com',
            password='testpass123'
        )
    
    def test_get_or_create_metadata(self):
        """Test get or create metadata"""
        seo, created = SEOService.get_or_create_metadata(
            self.user,
            defaults={
                'meta_title': 'User Profile',
                'meta_description': 'User profile page'
            }
        )
        self.assertTrue(created)
        self.assertEqual(seo.meta_title, 'User Profile')
        
        # Test get existing
        seo2, created2 = SEOService.get_or_create_metadata(self.user)
        self.assertFalse(created2)
        self.assertEqual(seo.pk, seo2.pk)
    
    def test_update_metadata(self):
        """Test update metadata"""
        SEOService.update_metadata(
            self.user,
            meta_title='Updated Title',
            meta_description='Updated Description'
        )
        
        content_type = ContentType.objects.get_for_model(self.user)
        seo = SEOMetadata.objects.get(content_type=content_type, object_id=self.user.pk)
        self.assertEqual(seo.meta_title, 'Updated Title')
    
    def test_delete_metadata(self):
        """Test delete metadata"""
        SEOService.update_metadata(
            self.user,
            meta_title='To Delete',
            meta_description='Will be deleted'
        )
        
        SEOService.delete_metadata(self.user)
        
        content_type = ContentType.objects.get_for_model(self.user)
        exists = SEOMetadata.objects.filter(
            content_type=content_type,
            object_id=self.user.pk
        ).exists()
        self.assertFalse(exists)


class RobotsServiceTest(TestCase):
    """Test Robots Service"""
    
    def test_generate_robots_txt(self):
        """Test robots.txt generation"""
        RobotsConfig.objects.create(
            user_agent='*',
            disallow='/admin/',
            order=1
        )
        RobotsConfig.objects.create(
            user_agent='Googlebot',
            allow='/api/',
            crawl_delay=10,
            order=2
        )
        
        robots_txt = RobotsService.generate_robots_txt()
        self.assertIn('User-agent: *', robots_txt)
        self.assertIn('Disallow: /admin/', robots_txt)
        self.assertIn('User-agent: Googlebot', robots_txt)
        self.assertIn('Crawl-delay: 10', robots_txt)
