"""Management command to check SEO health"""
from django.core.management.base import BaseCommand
from apps.seo.models import SEOMetadata, Redirect, SitemapConfig


class Command(BaseCommand):
    help = 'Check SEO health and provide recommendations'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== SEO Health Check ===\n'))
        
        total_metadata = SEOMetadata.objects.count()
        missing_og = SEOMetadata.objects.filter(og_image='').count()
        missing_twitter = SEOMetadata.objects.filter(twitter_image='').count()
        
        self.stdout.write(f'📊 SEO Metadata Statistics:')
        self.stdout.write(f'  Total entries: {total_metadata}')
        self.stdout.write(f'  Missing OG images: {missing_og}')
        self.stdout.write(f'  Missing Twitter images: {missing_twitter}\n')
        
        total_redirects = Redirect.objects.count()
        active_redirects = Redirect.objects.filter(is_active=True).count()
        unused_redirects = Redirect.objects.filter(hit_count=0, is_active=True).count()
        
        self.stdout.write(f'🔀 Redirect Statistics:')
        self.stdout.write(f'  Total redirects: {total_redirects}')
        self.stdout.write(f'  Active redirects: {active_redirects}')
        self.stdout.write(f'  Unused redirects: {unused_redirects}\n')
        
        total_configs = SitemapConfig.objects.count()
        enabled_configs = SitemapConfig.objects.filter(is_enabled=True).count()
        
        self.stdout.write(f'🗺️  Sitemap Configuration:')
        self.stdout.write(f'  Total configurations: {total_configs}')
        self.stdout.write(f'  Enabled configurations: {enabled_configs}\n')
        
        self.stdout.write(self.style.WARNING('💡 Recommendations:'))
        
        if missing_og > 0:
            self.stdout.write(f'  ⚠️  Add Open Graph images to {missing_og} entries')
        
        if missing_twitter > 0:
            self.stdout.write(f'  ⚠️  Add Twitter Card images to {missing_twitter} entries')
        
        if unused_redirects > 0:
            self.stdout.write(f'  ⚠️  Review {unused_redirects} unused redirects')
        
        if enabled_configs == 0:
            self.stdout.write(f'  ⚠️  No sitemap configurations enabled')
        
        if not any([missing_og, missing_twitter, unused_redirects, enabled_configs == 0]):
            self.stdout.write(self.style.SUCCESS('  ✅ Everything looks good!'))
        
        self.stdout.write('\n' + self.style.SUCCESS('=== Health Check Complete ==='))
