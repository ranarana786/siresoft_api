from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
import random
from service.models import Service, ServiceCategory 

class Command(BaseCommand):
    help = 'Populate Service model with dummy data'

    def handle(self, *args, **options):
        fake = Faker()

        categories = list(ServiceCategory.objects.all())
        if not categories:
            self.stdout.write(self.style.ERROR('No ServiceCategory found. Please create some first.'))
            return

        for _ in range(10):  
            name = fake.sentence(nb_words=3)
            category = random.choice(categories) 
            Service.objects.create(
                name=name,
                slug=slugify(name),
                category=category,
                service_type=random.choice(['development','design','marketing','consulting','support','custom']),
                short_description=fake.sentence(nb_words=6),
                description=fake.paragraph(nb_sentences=5),
                features=[fake.word() for _ in range(3)],
                requirements=[fake.word() for _ in range(2)],
                icon=f"icon-{fake.word()}",
                base_price=random.randint(50, 500),
                currency='USD',
                pricing_model=random.choice(['fixed','hourly','monthly','project','custom']),
                delivery_time=random.randint(1, 14),
                delivery_unit=random.choice(['hours','days','weeks','months']),
                revisions_included=random.randint(0,5),
                is_active=True,
                is_featured=random.choice([True, False]),
                display_order=random.randint(0,20)
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated 10 dummy services with random categories ✅'))