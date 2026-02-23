from django.core.management.base import BaseCommand
from django.utils.text import slugify
from service.models import ServiceCategory

class Command(BaseCommand):
    help = "Populate ServiceCategory model with default services"

    def handle(self, *args, **kwargs):
        categories = [
            "web and infrastructure",
            "Design and Branding",
            "Marketing and analytics",
            "Business Management System",
            "Data and Integrations"
        ]

        for index, name in enumerate(categories, start=1):
            obj, created = ServiceCategory.objects.get_or_create(
                name=name,
                defaults={
                    "slug": slugify(name),
                    "display_order": index,
                    "is_active": True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created: {name}"))
            else:
                self.stdout.write(f"Already exists: {name}")

        self.stdout.write(self.style.SUCCESS("✅ Service categories populated successfully!"))