from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import path
from django.http import FileResponse
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Profile
from .utils import generate_order_pdf

admin.site.site_header = "Oye Abbayi Admin"
admin.site.site_title = "Oye Abbayi Admin Portal"
admin.site.index_title = "Welcome to Oye Abbayi Management"


# ---------------- CATEGORY ----------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'icon_class')
    search_fields = ('name',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit:cover; border-radius:8px;" />')
        return "No Image"
    image_preview.short_description = 'Preview'


# ---------------- PRODUCT ----------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'category', 'price', 'unit', 'stock', 'delete_product')
    list_editable = ('unit',)
    list_filter = ('category',)
    search_fields = ('name', 'description')

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit:cover; border-radius:8px;" />')
        return mark_safe(f'<img src="/static/images/default_product.png" width="50" height="50" style="object-fit:cover; border-radius:8px;" />')
    image_preview.short_description = 'Preview'

    def delete_product(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        delete_url = reverse('admin:core_product_delete', args=[obj.id])
        return format_html('<a href="{}" class="button" style="background:#dc3545; color:white !important; padding:5px 10px; border-radius:5px; text-decoration:none;"><i class="fas fa-trash-alt"></i> Delete</a>', delete_url)
    
    delete_product.short_description = 'Actions'


# ---------------- CART ----------------
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('product', 'quantity')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    inlines = [CartItemInline]


# ---------------- ORDER ----------------
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price', 'get_total')
    readonly_fields = ('product', 'quantity', 'price', 'get_total')

    def get_total(self, obj):
        return obj.quantity * obj.price

    get_total.short_description = "Total"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'total_amount',
        'status',
        'phone_number',
        'pin_code',
        'address',
        'created_at',
        'download_bill_pdf',
    )
    list_editable = ('status',)
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'address', 'phone_number', 'pin_code')
    inlines = [OrderItemInline]

    def download_bill_pdf(self, obj):
        return mark_safe(f'<a href="download-pdf/{obj.id}/" class="button" style="background:#2d6a4f; color:white; padding:5px 10px; border-radius:5px; text-decoration:none;"><i class="fas fa-file-pdf"></i> Bill</a>')
    
    download_bill_pdf.short_description = 'Actions'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('download-pdf/<int:order_id>/', self.admin_site.admin_view(self.generate_bill), name='order_pdf'),
        ]
        return custom_urls + urls

    def generate_bill(self, request, order_id):
        from .models import Order
        order = Order.objects.get(id=order_id)
        buffer = generate_order_pdf(order)
        return FileResponse(buffer, as_attachment=True, filename=f"Oye_Abbayi_Bill_#{order.id}.pdf")


# ---------------- PROFILE ----------------
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')