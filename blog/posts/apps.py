from django.apps import AppConfig
from django.db.models.signals import post_migrate

class PostsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "blog.posts"

    def ready(self):
        from .models import Status

        def seed_statuses(sender, **kwargs):
            default_statuses = [
                {"name": "Draft"},
                {"name": "Published"},
                {"name": "Archived"},
            ]
            for status_data in default_statuses:
                Status.objects.get_or_create(name=status_data["name"])

        post_migrate.connect(seed_statuses, sender=self)
