from django.contrib import admin
from .models import Product, ProductImage, Order

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'in_stock', 'manufacturer']
    list_editable = ['category', 'price', 'in_stock', 'manufacturer']  # Allow inline editing
    list_filter = ['category', 'in_stock', 'manufacturer']
    search_fields = ['name', 'active_ingredient', 'manufacturer']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProductImageInline]

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'price', 'unit', 'in_stock', 'bonus')
        }),
        ('Medical Details', {
            'fields': ('active_ingredient', 'strength', 'manufacturer', 'indication', 'dosage', 'side_effects', 'contraindications', 'storage_requirements')
        }),
        ('Regulatory Info', {
            'fields': ('batch_info', 'expiry_info')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pharmacy_name', 'contact_person', 'phone', 'status', 'created_at']
    list_editable = ['status']  # Allow inline editing of order status
    list_filter = ['status', 'county', 'created_at']
    search_fields = ['pharmacy_name', 'contact_person', 'phone', 'email']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Pharmacy Information', {
            'fields': ('pharmacy_name', 'contact_person', 'phone', 'email')
        }),
        ('Delivery Address', {
            'fields': ('county', 'town', 'address')
        }),
        ('Order Details', {
            'fields': ('products', 'message')
        }),
        ('Status & Timestamps', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )

# Register ProductImage separately if needed
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_url', 'is_main']
    list_filter = ['is_main']
    search_fields = ['product__name']
