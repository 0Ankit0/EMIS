"""Management command to generate sitemap"""
from django.core.management.base import BaseCommand
from apps.seo.services import SitemapService


class Command(BaseCommand):
    help = 'Generate sitemap.xml file'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='sitemap.xml',
            help='Output file path'
        )
    
    def handle(self, *args, **options):
        output_file = options['output']
        
        self.stdout.write('Generating sitemap...')
        
        try:
            xml_content = SitemapService.generate_sitemap_xml()
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully generated sitemap: {output_file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error generating sitemap: {str(e)}')
            )
