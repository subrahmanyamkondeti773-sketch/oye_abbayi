import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GroceryMart.settings')
django.setup()

from core.models import Category, Product

def seed_data():
    # Categories
    veg, _ = Category.objects.get_or_create(name="Vegetables", description="Fresh and organic vegetables.")
    fruit, _ = Category.objects.get_or_create(name="Fruits", description="Sweet and juicy seasonal fruits.")
    dairy, _ = Category.objects.get_or_create(name="Dairy & Bakery", description="Milk, Bread, and more.")

    # Products
    Product.objects.get_or_create(
        category=veg, name="Fresh Tomato", description="Organic red tomatoes.",
        price=2.50, stock=100
    )
    Product.objects.get_or_create(
        category=veg, name="Spinach", description="Fresh green spinach leaves.",
        price=1.20, stock=50
    )
    Product.objects.get_or_create(
        category=fruit, name="Apple", description="Crunchy red apples.",
        price=3.00, stock=80
    )
    Product.objects.get_or_create(
        category=fruit, name="Banana", description="Sweet yellow bananas.",
        price=1.50, stock=120
    )
    Product.objects.get_or_create(
        category=dairy, name="Fresh Milk", description="Full cream cow milk.",
        price=1.80, stock=30
    )
    Product.objects.get_or_create(
        category=dairy, name="Whole Wheat Bread", description="Healthy and soft bread.",
        price=2.00, stock=40
    )

    print("Data seeded successfully!")

if __name__ == "__main__":
    seed_data()
