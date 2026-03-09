from django.apps import AppConfig


class NewsBriefConfig(AppConfig):
    name = 'news_brief'

    def ready(self):
        import news_brief.signals
        import os
        
        # Start the scheduler only in the main thread to prevent multiple instances
        if os.environ.get('RUN_MAIN', None) == 'true':
            try:
                from .scheduler import start_scheduler
                start_scheduler()
            except Exception as e:
                pass
