from django.core.management.base import BaseCommand
import yaml
from pathlib import Path
from news_brief.models import Publisher
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Imports RSS sources from the legacy sources.yaml file into the Publisher database model.'

    def handle(self, *args, **kwargs):
        # Path to the sources.yaml file
        config_path = Path('config/sources.yaml')
        
        if not config_path.exists():
            self.stdout.write(self.style.ERROR(f'Sources file not found at {config_path.absolute()}'))
            return

        with open(config_path, 'r') as file:
            try:
                data = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                self.stdout.write(self.style.ERROR(f'Error parsing YAML: {exc}'))
                return

        sources = data.get('news_sources', {})
        count = 0
        
        if not sources:
            self.stdout.write(self.style.WARNING('No sources found in YAML file.'))
            return

        for key, source_data in sources.items():
            name = source_data.get('name', key)
            base_url = source_data.get('base_url', '')
            rss_url = source_data.get('rss_feed', '')
            
            # Skip if no RSS URL (Google Search fallback case etc.)
            if not rss_url:
                self.stdout.write(self.style.WARNING(f'Skipping {name} (No RSS URL)'))
                continue
                
            publisher, created = Publisher.objects.get_or_create(
                name=name,
                defaults={
                    'base_url': base_url,
                    'rss_url': rss_url,
                    'is_active': True,
                    # We can assign country later or map it if known
                }
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created publisher: {name}'))
                count += 1
            else:
                self.stdout.write(self.style.WARNING(f'Publisher already exists: {name}'))
                
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} publishers from legacy config.'))
