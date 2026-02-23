# pricing/management/commands/create_pricing_plans.py

from django.core.management.base import BaseCommand
from django.db import transaction
from plans.models import PricingPlan, PlanFeature


class Command(BaseCommand):
    help = 'Recreate all pricing plans (Basic, Pro, Enterprise, Ultimate)'

    @transaction.atomic
    def handle(self, *args, **options):

        self.stdout.write(self.style.WARNING('⚠ Deleting old pricing data...'))

        # 🔥 Delete ALL existing pricing data
        PlanFeature.objects.all().delete()
        PricingPlan.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Old data deleted successfully.\n'))

        plans_data = [
            {
                'name': 'Business Basic',
                'plan_type': 'basic',
                'tagline': 'Essential tools for a professional start and personal presence.',
                'price': 29.00,
                'billing_period': 'monthly',
                'is_popular': True,
                'badge_text': 'Popular',
                'button_text': 'Add to Cart',
                'order': 1,
                'features': [
                    ('Core Business Logic', True),
                    ('Standard Support', True),
                    ('Advanced Analytics', False),
                    ('Custom API Access', False),
                    ('Dedicated Manager', False),
                    ('Unlimited Cloud Storage', False),
                ]
            },
            {
                'name': 'Business Pro',
                'plan_type': 'pro',
                'tagline': 'Advanced features for growing businesses.',
                'price': 79.00,
                'billing_period': 'monthly',
                'is_featured': True,
                'badge_text': 'Best Value',
                'button_text': 'Add to Cart',
                'order': 2,
                'features': [
                    ('Core Business Logic', True),
                    ('Standard Support', True),
                    ('Advanced Analytics', True),
                    ('Custom API Access', True),
                    ('Dedicated Manager', False),
                    ('Unlimited Cloud Storage', False),
                ]
            },
            {
                'name': 'Business Enterprise',
                'plan_type': 'enterprise',
                'tagline': 'Complete solution for large organizations.',
                'price': 199.00,
                'billing_period': 'monthly',
                'is_featured': True,
                'badge_text': 'Enterprise',
                'button_text': 'Contact Sales',
                'order': 3,
                'features': [
                    ('Core Business Logic', True),
                    ('Standard Support', True),
                    ('Advanced Analytics', True),
                    ('Custom API Access', True),
                    ('Dedicated Manager', True),
                    ('Unlimited Cloud Storage', True),
                ]
            },
            {
                'name': 'Business Ultimate',
                'plan_type': 'ultimate',
                'tagline': 'All-inclusive premium solution with priority everything.',
                'price': 299.00,
                'billing_period': 'monthly',
                'is_featured': True,
                'badge_text': 'Ultimate',
                'button_text': 'Get Started',
                'order': 4,
                'features': [
                    ('Core Business Logic', True),
                    ('Standard Support', True),
                    ('Advanced Analytics', True),
                    ('Custom API Access', True),
                    ('Dedicated Manager', True),
                    ('Unlimited Cloud Storage', True),
                    ('Priority 24/7 Support', True),
                    ('White Label Solution', True),
                ]
            }
        ]

        self.stdout.write(self.style.SUCCESS('🚀 Creating new pricing plans...\n'))

        for plan_data in plans_data:
            features = plan_data.pop('features')

            plan = PricingPlan.objects.create(
                **plan_data,
                is_active=True
            )

            self.stdout.write(self.style.SUCCESS(f'✓ Created plan: {plan.name}'))

            for idx, (feature_name, is_included) in enumerate(features, 1):
                PlanFeature.objects.create(
                    plan=plan,
                    name=feature_name,
                    is_included=is_included,
                    order=idx
                )

                status = "✓" if is_included else "✗"
                self.stdout.write(f'  {status} {feature_name}')

        self.stdout.write(self.style.SUCCESS('\n✅ All 4 pricing plans created successfully!'))