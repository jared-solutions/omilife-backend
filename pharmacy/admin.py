import csv
from django.contrib import admin
from django.http import HttpResponse
from .models import Product, ProductImage, Order, HospitalFacility, ProductBatch, Invoice, InvoiceItem, PaymentReceipt, OrderSalesNote

# Customize Admin Site Branding
admin.site.site_header = "Omilife Pharmaceuticals Management Portal"
admin.site.site_title = "Omilife Admin"
admin.site.index_title = "Order Dispatch & Inventory Control"

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'in_stock', 'manufacturer']
    list_editable = ['in_stock']
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

def export_orders_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="omilife_orders.csv"'
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Pharmacy Name', 'Contact Person', 'Phone', 'Email', 'County', 'Town', 'Address', 'Products', 'Status', 'Date'])
    for order in queryset:
        writer.writerow([order.id, order.pharmacy_name, order.contact_person, order.phone, order.email, order.county, order.town, order.address, order.products, order.status, order.created_at.strftime('%Y-%m-%d %H:%M')])
    return response
export_orders_to_csv.short_description = "Export selected orders to CSV"

def mark_as_confirmed(modeladmin, request, queryset):
    queryset.update(status='confirmed')
mark_as_confirmed.short_description = "Mark selected as Confirmed (Sales Called)"

def mark_as_shipped(modeladmin, request, queryset):
    queryset.update(status='shipped')
mark_as_shipped.short_description = "Mark selected as Shipped (In Transit)"

def mark_as_delivered(modeladmin, request, queryset):
    queryset.update(status='delivered')
mark_as_delivered.short_description = "Mark selected as Delivered"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'pharmacy_name', 'contact_person', 'phone', 'county', 'status', 'created_at']
    list_editable = ['status']
    list_filter = ['status', 'county', 'created_at']
    search_fields = ['pharmacy_name', 'contact_person', 'phone', 'email', 'town']
    readonly_fields = ['created_at', 'updated_at']
    actions = [mark_as_confirmed, mark_as_shipped, mark_as_delivered, export_orders_to_csv]

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

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_url', 'is_main']
    list_filter = ['is_main']
    search_fields = ['product__name']


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 0

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'facility_name', 'county', 'grand_total', 'payment_status', 'date']
    list_filter = ['payment_status', 'county', 'payment_method']
    search_fields = ['invoice_number', 'facility_name', 'ppb_license']
    inlines = [InvoiceItemInline]

@admin.register(PaymentReceipt)
class PaymentReceiptAdmin(admin.ModelAdmin):
    list_display = ['receipt_number', 'invoice_number', 'facility_name', 'amount', 'payment_method', 'date']
    list_filter = ['payment_method']
    search_fields = ['receipt_number', 'invoice_number', 'facility_name', 'reference_number']

@admin.register(ProductBatch)
class ProductBatchAdmin(admin.ModelAdmin):
    list_display = ['medicine_name', 'batch_number', 'exp_date', 'quantity_packs', 'quarantine_status']
    list_filter = ['quarantine_status']
    search_fields = ['medicine_name', 'batch_number', 'sku']

@admin.register(HospitalFacility)
class HospitalFacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'facility_type', 'county', 'ppb_license', 'phone']
    list_filter = ['county', 'facility_type']
    search_fields = ['name', 'ppb_license', 'contact_person']
