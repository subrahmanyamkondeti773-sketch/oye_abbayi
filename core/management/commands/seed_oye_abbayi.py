from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Category, Product
class Command(BaseCommand):
    help = 'Seed initial data for Oye Abbayi'

    def handle(self, *args, **kwargs):
        # 1. Categories
        categories_data = [
            {'name': 'Groceries', 'icon_class': 'fas fa-shopping-basket'},
            {'name': 'Vegetables', 'icon_class': 'fas fa-carrot'},
            {'name': 'Fruits', 'icon_class': 'fas fa-apple-alt'},
            {'name': 'Dairy & Bakery', 'icon_class': 'fas fa-bread-slice'},
        ]

        cats = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(name=cat_data['name'])
            cat.icon_class = cat_data['icon_class']
            cat.save()
            cats[cat.name] = cat
            status = "Created" if created else "Updated"
            self.stdout.write(self.style.SUCCESS(f"{status} category: {cat.name}"))

        # 2. Products
        products_data = [
            # Vegetables
            {'name': 'Fresh Onion', 'price': 30, 'unit': 'kg', 'category': 'Vegetables', 'desc': 'Farmer fresh red onions.'},
            {'name': 'Organic Tomato', 'price': 40, 'unit': 'kg', 'category': 'Vegetables', 'desc': 'Juicy organic tomatoes.'},
            {'name': 'Potato', 'price': 25, 'unit': 'kg', 'category': 'Vegetables', 'desc': 'Premium quality potatoes.'},
            # Fruits
            {'name': 'Sweet Apple', 'price': 120, 'unit': 'kg', 'category': 'Fruits', 'desc': 'Crispy red apples from the hills.'},
            {'name': 'Banana', 'price': 50, 'unit': 'dz', 'category': 'Fruits', 'desc': 'Energizing yellow bananas.'},
            # Dairy
            {'name': 'Pure Milk', 'price': 60, 'unit': 'L', 'category': 'Dairy & Bakery', 'desc': 'Fresh farm milk.'},
            {'name': 'Butter', 'price': 50, 'unit': 'pkt', 'category': 'Dairy & Bakery', 'desc': 'Creamy unsalted butter.'},
            # Groceries
            {'name': 'Basmati Rice', 'price': 90, 'unit': 'kg', 'category': 'Groceries', 'desc': 'Long grain aromatic rice.'},
            {'name': 'Sugar', 'price': 45, 'unit': 'kg', 'category': 'Groceries', 'desc': 'Crystal clear pure sugar.'},
        ]

        for p_data in products_data:
            product, created = Product.objects.get_or_create(
                name=p_data['name'],
                defaults={
                    'category': cats[p_data['category']],
                    'price': p_data['price'],
                    'unit': p_data['unit'],
                    'stock': 100,
                    'description': p_data['desc']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created product: {product.name}"))
            else:
                self.stdout.write(self.style.SUCCESS(f"Product exists: {product.name}"))

        # 3. Superuser (Standard admin for Render if none exist)
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS("Created superuser: admin (password: admin123)"))
