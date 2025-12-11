"""Management command to generate robots.txt"""
from django.core.management.base import BaseCommand
from apps.seo.services import RobotsService


class Command(BaseCommand):
    help = 'Generate robots.txt file'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='robots.txt',
            help='Output file path'
        )
    
    def handle(self, *args, **options):
        output_file = options['output']
        
        self.stdout.write('Generating robots.txt...')
        
        try:
            robots_content = RobotsService.generate_robots_txt()
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(robots_content)
            
            self.stdout.write(
                self.style.SUCCESS(f'Successfully generated robots.txt: {output_file}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error generating robots.txt: {str(e)}')
            )
