from django.core.management.base import BaseCommand
from core.models import Category

class Command(BaseCommand):
    help = 'Seed initial categories for Oye Abbayi'

    def handle(self, *args, **kwargs):
        categories = [
            {'name': 'Groceries', 'icon_class': 'fas fa-shopping-basket'},
            {'name': 'Vegetables', 'icon_class': 'fas fa-carrot'},
            {'name': 'Fruits', 'icon_class': 'fas fa-apple-alt'},
            {'name': 'Dairy & Bakery', 'icon_class': 'fas fa-bread-slice'},
        ]

        for cat_data in categories:
            cat, created = Category.objects.get_or_create(name=cat_data['name'])
            cat.icon_class = cat_data['icon_class']
            cat.save()
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {cat.name}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Updated category: {cat.name}"))
