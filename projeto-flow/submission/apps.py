from django.apps import AppConfig


class SubmissionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'submission'
    
    def ready(self):
        import submission.signals  # noqa: F401
