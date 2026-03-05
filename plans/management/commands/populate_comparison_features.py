# services/management/commands/populate_comparison_data.py
"""
Django Management Command to Populate Service Comparison Data
Format matches existing API: features with values array containing plan_id, plan_name, value

Usage: python manage.py populate_comparison_data
"""

from django.core.management.base import BaseCommand
from plans.models import PricingPlan, PlanComparison, PlanComparisonValue
from service.models import Service# Your existing pricing plans



class Command(BaseCommand):
    help = 'Populate comparison features and values for all services'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating comparison data...'))

        # Get existing pricing plans
        try:
            basic_plan = PricingPlan.objects.get(slug='business-basic')
            pro_plan = PricingPlan.objects.get(slug='business-pro')
            enterprise_plan = PricingPlan.objects.get(slug='business-enterprise')
        except PricingPlan.DoesNotExist:
            self.stdout.write(self.style.ERROR('Error: Pricing plans not found!'))
            self.stdout.write('Please run: python manage.py create_pricing_plans first')
            return

        # Service comparison data for all 7 services
        comparison_data = {
            'Web Design & Branding': [
                {
                    'name': 'Number of Pages',
                    'category': 'Design Features',
                    'description': 'Total number of pages included',
                    'values': {
                        'basic': '5 Pages',
                        'pro': '10 Pages',
                        'enterprise': 'Unlimited Pages'
                    }
                },
                {
                    'name': 'Design Type',
                    'category': 'Design Features',
                    'description': 'Level of design customization',
                    'values': {
                        'basic': 'Template Based',
                        'pro': 'Semi-Custom Design',
                        'enterprise': 'Fully Custom Design'
                    }
                },
                {
                    'name': 'Logo Design',
                    'category': 'Branding',
                    'description': 'Logo design service included',
                    'values': {
                        'basic': 'Not Included',
                        'pro': 'Basic Logo',
                        'enterprise': 'Premium Logo Package'
                    }
                },
                {
                    'name': 'Responsive Design',
                    'category': 'Technical',
                    'description': 'Mobile-friendly responsive design',
                    'values': {
                        'basic': 'Yes',
                        'pro': 'Yes',
                        'enterprise': 'Yes + Tablet Optimized'
                    }
                },
                {
                    'name': 'SEO Optimization',
                    'category': 'Marketing',
                    'description': 'Search engine optimization',
                    'values': {
                        'basic': 'Basic SEO',
                        'pro': 'Advanced SEO',
                        'enterprise': 'Premium SEO + Analytics'
                    }
                },
                {
                    'name': 'CMS Access',
                    'category': 'Technical',
                    'description': 'Content management system',
                    'values': {
                        'basic': 'No',
                        'pro': 'Yes - WordPress',
                        'enterprise': 'Yes - Custom CMS'
                    }
                },
                {
                    'name': 'E-commerce',
                    'category': 'Features',
                    'description': 'Online shopping functionality',
                    'values': {
                        'basic': 'No',
                        'pro': 'Basic Shop (10 products)',
                        'enterprise': 'Advanced Shop (Unlimited)'
                    }
                },
                {
                    'name': 'SSL Certificate',
                    'category': 'Security',
                    'description': 'HTTPS security certificate',
                    'values': {
                        'basic': 'No',
                        'pro': 'Free SSL',
                        'enterprise': 'Premium SSL'
                    }
                },
                {
                    'name': 'Monthly Maintenance',
                    'category': 'Support',
                    'description': 'Monthly maintenance hours',
                    'values': {
                        'basic': 'No',
                        'pro': '2 Hours/Month',
                        'enterprise': 'Unlimited Hours'
                    }
                },
                {
                    'name': 'Delivery Time',
                    'category': 'Timeline',
                    'description': 'Project completion time',
                    'values': {
                        'basic': '30 Days',
                        'pro': '45 Days',
                        'enterprise': '60 Days'
                    }
                },
            ],
            'Business CRM': [
                {
                    'name': 'User Accounts',
                    'category': 'Access',
                    'description': 'Number of user accounts',
                    'values': {
                        'basic': '3 Users',
                        'pro': '10 Users',
                        'enterprise': 'Unlimited Users'
                    }
                },
                {
                    'name': 'Contact Storage',
                    'category': 'Data',
                    'description': 'Maximum contacts storage',
                    'values': {
                        'basic': '1,000 Contacts',
                        'pro': '10,000 Contacts',
                        'enterprise': 'Unlimited Contacts'
                    }
                },
                {
                    'name': 'Live Chat',
                    'category': 'Communication',
                    'description': 'Live chat widget integration',
                    'values': {
                        'basic': 'No',
                        'pro': 'Yes',
                        'enterprise': 'Yes + AI Assistant'
                    }
                },
                {
                    'name': 'Custom Forms',
                    'category': 'Features',
                    'description': 'Customizable feedback forms',
                    'values': {
                        'basic': '3 Forms',
                        'pro': '10 Forms',
                        'enterprise': 'Unlimited Forms'
                    }
                },
                {
                    'name': 'Email Automation',
                    'category': 'Automation',
                    'description': 'Automated email campaigns',
                    'values': {
                        'basic': 'No',
                        'pro': 'Basic Automation',
                        'enterprise': 'Advanced Automation'
                    }
                },
                {
                    'name': 'Sales Pipeline',
                    'category': 'Sales',
                    'description': 'Sales pipeline management',
                    'values': {
                        'basic': 'Basic Pipeline',
                        'pro': 'Advanced Pipeline',
                        'enterprise': 'Custom Pipeline + AI'
                    }
                },
                {
                    'name': 'Invoicing',
                    'category': 'Billing',
                    'description': 'Invoice generation system',
                    'values': {
                        'basic': 'No',
                        'pro': 'Basic Invoicing',
                        'enterprise': 'Advanced + Auto-billing'
                    }
                },
                {
                    'name': 'Cart Recovery',
                    'category': 'E-commerce',
                    'description': 'Abandoned cart recovery',
                    'values': {
                        'basic': 'No',
                        'pro': 'No',
                        'enterprise': 'Yes'
                    }
                },
                {
                    'name': 'Analytics',
                    'category': 'Reports',
                    'description': 'Analytics and reporting',
                    'values': {
                        'basic': 'Basic Reports',
                        'pro': 'Advanced Analytics',
                        'enterprise': 'Custom Dashboards'
                    }
                },
                {
                    'name': 'API Access',
                    'category': 'Integration',
                    'description': 'API integration access',
                    'values': {
                        'basic': 'No',
                        'pro': 'Limited API',
                        'enterprise': 'Full API Access'
                    }
                },
            ],
            'Logo Design': [
                {
                    'name': 'Logo Concepts',
                    'category': 'Design',
                    'description': 'Initial logo design concepts',
                    'values': {
                        'basic': '2 Concepts',
                        'pro': '5 Concepts',
                        'enterprise': '10 Concepts'
                    }
                },
                {
                    'name': 'Revisions',
                    'category': 'Design',
                    'description': 'Number of revision rounds',
                    'values': {
                        'basic': '3 Revisions',
                        'pro': '5 Revisions',
                        'enterprise': 'Unlimited Revisions'
                    }
                },
                {
                    'name': 'File Formats',
                    'category': 'Delivery',
                    'description': 'Provided file formats',
                    'values': {
                        'basic': 'PNG, JPG',
                        'pro': 'PNG, JPG, SVG, PDF',
                        'enterprise': 'All Formats + Source'
                    }
                },
                {
                    'name': 'Color Variations',
                    'category': 'Design',
                    'description': 'Logo color variations',
                    'values': {
                        'basic': '1 Color Scheme',
                        'pro': '3 Color Schemes',
                        'enterprise': 'Unlimited Colors'
                    }
                },
                {
                    'name': 'Brand Guide',
                    'category': 'Branding',
                    'description': 'Brand style guidelines',
                    'values': {
                        'basic': 'No',
                        'pro': 'Basic Guide',
                        'enterprise': 'Complete Brand Book'
                    }
                },
                {
                    'name': 'Business Cards',
                    'category': 'Collateral',
                    'description': 'Business card design',
                    'values': {
                        'basic': 'No',
                        'pro': 'Yes',
                        'enterprise': 'Yes + Letterhead'
                    }
                },
                {
                    'name': 'Letterhead',
                    'category': 'Collateral',
                    'description': 'Letterhead design',
                    'values': {
                        'basic': 'No',
                        'pro': 'No',
                        'enterprise': 'Yes'
                    }
                },
                {
                    'name': 'Social Media Kit',
                    'category': 'Digital',
                    'description': 'Social media templates',
                    'values': {
                        'basic': 'No',
                        'pro': 'Basic Kit (3 templates)',
                        'enterprise': 'Complete Kit (10+ templates)'
                    }
                },
                {
                    'name': 'Turnaround',
                    'category': 'Timeline',
                    'description': 'Project delivery time',
                    'values': {
                        'basic': '7 Days',
                        'pro': '10 Days',
                        'enterprise': '14 Days'
                    }
                },
                {
                    'name': 'Commercial Rights',
                    'category': 'Legal',
                    'description': 'Full commercial usage rights',
                    'values': {
                        'basic': 'Yes',
                        'pro': 'Yes',
                        'enterprise': 'Yes + Trademark Support'
                    }
                },
            ],
            'Inventory Control': [
                {
                    'name': 'Product SKUs',
                    'category': 'Capacity',
                    'description': 'Maximum product SKUs',
                    'values': {
                        'basic': '500 SKUs',
                        'pro': '5,000 SKUs',
                        'enterprise': 'Unlimited SKUs'
                    }
                },
                {
                    'name': 'Warehouse Locations',
                    'category': 'Multi-location',
                    'description': 'Number of warehouse locations',
                    'values': {
                        'basic': '1 Location',
                        'pro': '3 Locations',
                        'enterprise': 'Unlimited Locations'
                    }
                },
                {
                    'name': 'Barcode Scanning',
                    'category': 'Features',
                    'description': 'Barcode scanner support',
                    'values': {
                        'basic': 'No',
                        'pro': 'Yes',
                        'enterprise': 'Yes + QR Codes'
                    }
                },
                {
                    'name': 'Purchase Orders',
                    'category': 'Procurement',
                    'description': 'Purchase order management',
                    'values': {
                        'basic': 'Basic PO',
                        'pro': 'Advanced PO',
                        'enterprise': 'Custom PO + Auto-reorder'
                    }
                },
                {
                    'name': 'Stock Alerts',
                    'category': 'Automation',
                    'description': 'Low stock notifications',
                    'values': {
                        'basic': 'Email Only',
                        'pro': 'Email + SMS',
                        'enterprise': 'Multi-channel + AI Predict'
                    }
                },
                {
                    'name': 'Reports',
                    'category': 'Analytics',
                    'description': 'Inventory reporting',
                    'values': {
                        'basic': 'Basic Reports',
                        'pro': 'Advanced Reports',
                        'enterprise': 'Custom Dashboards'
                    }
                },
                {
                    'name': 'Sales Integration',
                    'category': 'Integration',
                    'description': 'POS system integration',
                    'values': {
                        'basic': 'No',
                        'pro': 'Yes',
                        'enterprise': 'Yes + Multiple Systems'
                    }
                },
                {
                    'name': 'Supplier Portal',
                    'category': 'Vendors',
                    'description': 'Supplier management portal',
                    'values': {
                        'basic': 'Basic List',
                        'pro': 'Advanced Management',
                        'enterprise': 'Full Portal + Auto-order'
                    }
                },
                {
                    'name': 'Mobile App',
                    'category': 'Access',
                    'description': 'Mobile application access',
                    'values': {
                        'basic': 'No',
                        'pro': 'Yes (iOS/Android)',
                        'enterprise': 'Yes + Offline Mode'
                    }
                },
                {
                    'name': 'API Integration',
                    'category': 'Technical',
                    'description': 'REST API access',
                    'values': {
                        'basic': 'No',
                        'pro': 'Limited API',
                        'enterprise': 'Full API Access'
                    }
                },
            ],
            'Virtual Machines': [
                {
                    'name': 'VM Instances',
                    'category': 'Capacity',
                    'description': 'Number of virtual machines',
                    'values': {
                        'basic': '1 VM',
                        'pro': '5 VMs',
                        'enterprise': 'Unlimited VMs'
                    }
                },
                {
                    'name': 'RAM per VM',
                    'category': 'Resources',
                    'description': 'Memory allocation per VM',
                    'values': {
                        'basic': '2 GB RAM',
                        'pro': '8 GB RAM',
                        'enterprise': 'Custom RAM'
                    }
                },
                {
                    'name': 'Storage per VM',
                    'category': 'Resources',
                    'description': 'Disk storage per VM',
                    'values': {
                        'basic': '50 GB SSD',
                        'pro': '200 GB SSD',
                        'enterprise': 'Custom Storage'
                    }
                },
                {
                    'name': 'CPU Cores',
                    'category': 'Resources',
                    'description': 'CPU cores per VM',
                    'values': {
                        'basic': '2 vCPUs',
                        'pro': '4 vCPUs',
                        'enterprise': 'Custom vCPUs'
                    }
                },
                {
                    'name': 'Operating System',
                    'category': 'Software',
                    'description': 'Supported OS options',
                    'values': {
                        'basic': 'Windows/Linux',
                        'pro': 'Windows/Linux/Ubuntu',
                        'enterprise': 'Any OS + Custom Images'
                    }
                },
                {
                    'name': 'Backups',
                    'category': 'Data Protection',
                    'description': 'Automated backup frequency',
                    'values': {
                        'basic': 'Weekly Backup',
                        'pro': 'Daily Backup',
                        'enterprise': 'Hourly + Snapshots'
                    }
                },
                {
                    'name': 'Remote Access',
                    'category': 'Connectivity',
                    'description': 'Remote desktop access',
                    'values': {
                        'basic': 'RDP/SSH',
                        'pro': 'RDP/SSH + VPN',
                        'enterprise': 'All Protocols + Dedicated IP'
                    }
                },
                {
                    'name': 'Scalability',
                    'category': 'Features',
                    'description': 'Resource scaling options',
                    'values': {
                        'basic': 'Fixed Resources',
                        'pro': 'Manual Scaling',
                        'enterprise': 'Auto-scaling'
                    }
                },
                {
                    'name': 'Support',
                    'category': 'Support',
                    'description': 'Technical support level',
                    'values': {
                        'basic': 'Email Support',
                        'pro': '24/7 Chat Support',
                        'enterprise': 'Dedicated Manager'
                    }
                },
                {
                    'name': 'Uptime SLA',
                    'category': 'Reliability',
                    'description': 'Service level agreement',
                    'values': {
                        'basic': '99% Uptime',
                        'pro': '99.5% Uptime',
                        'enterprise': '99.9% Uptime'
                    }
                },
            ],
            'Hosting': [
                {
                    'name': 'Storage Space',
                    'category': 'Resources',
                    'description': 'Web hosting storage',
                    'values': {
                        'basic': '2 GB',
                        'pro': '50 GB',
                        'enterprise': 'Unlimited'
                    }
                },
                {
                    'name': 'Bandwidth',
                    'category': 'Resources',
                    'description': 'Monthly bandwidth limit',
                    'values': {
                        'basic': '20 GB/month',
                        'pro': '500 GB/month',
                        'enterprise': 'Unlimited'
                    }
                },
                {
                    'name': 'Domains',
                    'category': 'Domains',
                    'description': 'Number of hosted domains',
                    'values': {
                        'basic': '1 Domain',
                        'pro': '5 Domains',
                        'enterprise': 'Unlimited Domains'
                    }
                },
                {
                    'name': 'Email Accounts',
                    'category': 'Email',
                    'description': 'Business email accounts',
                    'values': {
                        'basic': '5 Accounts',
                        'pro': '25 Accounts',
                        'enterprise': 'Unlimited Accounts'
                    }
                },
                {
                    'name': 'SSL Certificate',
                    'category': 'Security',
                    'description': 'HTTPS security certificate',
                    'values': {
                        'basic': 'Free SSL',
                        'pro': 'Free Wildcard SSL',
                        'enterprise': 'Premium SSL + EV'
                    }
                },
                {
                    'name': 'Free Domain',
                    'category': 'Domains',
                    'description': 'Free domain registration',
                    'values': {
                        'basic': '1 Year Free',
                        'pro': '1 Year Free',
                        'enterprise': '2 Years Free'
                    }
                },
                {
                    'name': 'Backups',
                    'category': 'Data Protection',
                    'description': 'Backup frequency',
                    'values': {
                        'basic': 'Weekly Backup',
                        'pro': 'Daily Backup',
                        'enterprise': 'Real-time Backup'
                    }
                },
                {
                    'name': 'Control Panel',
                    'category': 'Management',
                    'description': 'Hosting control panel',
                    'values': {
                        'basic': 'cPanel',
                        'pro': 'cPanel + Softaculous',
                        'enterprise': 'Custom Panel'
                    }
                },
                {
                    'name': 'Server Location',
                    'category': 'Infrastructure',
                    'description': 'Data center location',
                    'values': {
                        'basic': 'US-based',
                        'pro': 'US + EU',
                        'enterprise': 'Multi-region Choice'
                    }
                },
                {
                    'name': 'Support',
                    'category': 'Support',
                    'description': 'Customer support',
                    'values': {
                        'basic': 'Email Support',
                        'pro': '24/7 Chat Support',
                        'enterprise': 'Priority Phone Support'
                    }
                },
            ],
            'ETL': [
                {
                    'name': 'Data Sources',
                    'category': 'Integration',
                    'description': 'Number of data sources',
                    'values': {
                        'basic': '5 Sources',
                        'pro': '20 Sources',
                        'enterprise': 'Unlimited Sources'
                    }
                },
                {
                    'name': 'Monthly Volume',
                    'category': 'Capacity',
                    'description': 'Data processing volume',
                    'values': {
                        'basic': '10 GB/month',
                        'pro': '100 GB/month',
                        'enterprise': 'Unlimited'
                    }
                },
                {
                    'name': 'Transformations',
                    'category': 'Processing',
                    'description': 'Data transformation rules',
                    'values': {
                        'basic': 'Basic Transforms',
                        'pro': 'Advanced Transforms',
                        'enterprise': 'Custom Logic + Python'
                    }
                },
                {
                    'name': 'Scheduling',
                    'category': 'Automation',
                    'description': 'Pipeline scheduling',
                    'values': {
                        'basic': 'Daily Schedule',
                        'pro': 'Hourly Schedule',
                        'enterprise': 'Real-time Streaming'
                    }
                },
                {
                    'name': 'Data Quality',
                    'category': 'Quality',
                    'description': 'Quality validation checks',
                    'values': {
                        'basic': 'Basic Validation',
                        'pro': 'Advanced Rules',
                        'enterprise': 'Custom ML Validation'
                    }
                },
                {
                    'name': 'Error Handling',
                    'category': 'Reliability',
                    'description': 'Error recovery system',
                    'values': {
                        'basic': 'Email Notifications',
                        'pro': 'Auto-retry + Alerts',
                        'enterprise': 'Custom Logic + Rollback'
                    }
                },
                {
                    'name': 'Data Warehouse',
                    'category': 'Storage',
                    'description': 'Data warehouse integration',
                    'values': {
                        'basic': 'No',
                        'pro': 'Basic DW (PostgreSQL)',
                        'enterprise': 'Enterprise DW (Snowflake/Redshift)'
                    }
                },
                {
                    'name': 'API Support',
                    'category': 'Integration',
                    'description': 'API protocol support',
                    'values': {
                        'basic': 'REST APIs',
                        'pro': 'REST + SOAP',
                        'enterprise': 'All Protocols + GraphQL'
                    }
                },
                {
                    'name': 'Monitoring',
                    'category': 'Observability',
                    'description': 'Pipeline monitoring',
                    'values': {
                        'basic': 'Basic Logs',
                        'pro': 'Advanced Dashboard',
                        'enterprise': 'Real-time Monitoring + AI'
                    }
                },
                {
                    'name': 'Support',
                    'category': 'Support',
                    'description': 'Technical support level',
                    'values': {
                        'basic': 'Email Support',
                        'pro': '24/7 Chat Support',
                        'enterprise': 'Dedicated Data Engineer'
                    }
                },
            ],
        }

        # Create comparison features and values
        order = 0
        for service_name, features in comparison_data.items():
            self.stdout.write(f'\n{service_name}:')
            service = service, _ = Service.objects.get_or_create(name=service_name)
            
            for feature_data in features:
                order += 1
                
                # Create or update feature
                feature, created = PlanComparison.objects.update_or_create(
                    service=service,
                    name=feature_data['name'],
                    defaults={
                        'category': feature_data['category'],
                        'description': feature_data['description'],
                        'order': order
                    }
                )
                
                if created:
                    self.stdout.write(f'  ✓ Created: {feature.name}')
                else:
                    self.stdout.write(f'  Updated: {feature.name}')
                
                # Create values for each plan
                values = feature_data['values']
                
                # Basic plan value
                PlanComparisonValue.objects.update_or_create(
                    comparison_feature=feature,
                    plan=basic_plan,
                    defaults={
                        'value': values['basic'],
                        'is_available': values['basic'].lower() not in ['no', 'n/a', '-']
                    }
                )
                
                # Pro plan value
                PlanComparisonValue.objects.update_or_create(
                    comparison_feature=feature,
                    plan=pro_plan,
                    defaults={
                        'value': values['pro'],
                        'is_available': values['pro'].lower() not in ['no', 'n/a', '-']
                    }
                )
                
                # Enterprise plan value
                PlanComparisonValue.objects.update_or_create(
                    comparison_feature=feature,
                    plan=enterprise_plan,
                    defaults={
                        'value': values['enterprise'],
                        'is_available': values['enterprise'].lower() not in ['no', 'n/a', '-']
                    }
                )

        self.stdout.write(self.style.SUCCESS('\n✅ All comparison data populated successfully!'))
        self.stdout.write('\nYou can now access the comparison API at:')
        self.stdout.write('  GET /api/comparison/features/')