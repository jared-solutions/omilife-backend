from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Gastrointestinal', 'Gastrointestinal'),
        ('Respiratory', 'Respiratory'),
        ('Cardiovascular', 'Cardiovascular'),
        ('Mental Health', 'Mental Health'),
        ('Rheumatology', 'Rheumatology'),
    ]

    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.CharField(max_length=20)  # e.g., "KSh 1,529"
    unit = models.CharField(max_length=100)  # e.g., "per pack (14 tablets)"
    in_stock = models.BooleanField(default=True)
    bonus = models.CharField(max_length=50, blank=True, null=True)  # e.g., "10+1"

    # Details about the medicine
    active_ingredient = models.CharField(max_length=200)
    strength = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=200)
    indication = models.TextField()
    dosage = models.TextField()
    side_effects = models.TextField()
    contraindications = models.TextField()
    storage_requirements = models.CharField(max_length=200)
    batch_info = models.CharField(max_length=100)
    expiry_info = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField()  # Using URLs for images as they're stored in the frontend for now
    is_main = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - Image"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    # Info about the pharmacy or organization
    pharmacy_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    # Where to deliver the order
    county = models.CharField(max_length=50)
    town = models.CharField(max_length=100)
    address = models.TextField()

    # Details of what was ordered
    products = models.TextField()  # Text description of products and quantities
    message = models.TextField(blank=True, null=True)  # Additional notes

    # Current status of the order
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order by {self.contact_person} from {self.pharmacy_name}"


class HospitalFacility(models.Model):
    name = models.CharField(max_length=255)
    facility_type = models.CharField(max_length=100, default='Private Level 5')
    county = models.CharField(max_length=100, default='Nairobi')
    address = models.TextField(blank=True, default='')
    ppb_license = models.CharField(max_length=100)
    kra_pin = models.CharField(max_length=100, blank=True, default='')
    contact_person = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=1000000.00)
    outstanding_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tier = models.CharField(max_length=50, default='Standard Hospital')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.county})"


class ProductBatch(models.Model):
    sku = models.CharField(max_length=50)
    medicine_name = models.CharField(max_length=200)
    strength = models.CharField(max_length=100, blank=True, default='')
    batch_number = models.CharField(max_length=100, unique=True)
    mfg_date = models.DateField()
    exp_date = models.DateField()
    quantity_packs = models.IntegerField(default=100)
    quarantine_status = models.CharField(max_length=50, default='RELEASED')
    warehouse_location = models.CharField(max_length=200, default='Warehouse Ambient Aisle')
    unit_cost_kes = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    selling_price_kes = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.medicine_name} - Batch {self.batch_number}"


class Invoice(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PAID', 'PAID'),
        ('PENDING', 'PENDING'),
        ('OVERDUE', 'OVERDUE'),
        ('PARTIAL', 'PARTIAL'),
    ]

    invoice_number = models.CharField(max_length=50, unique=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    facility_name = models.CharField(max_length=255)
    facility_type = models.CharField(max_length=100, default='Private Level 5')
    county = models.CharField(max_length=100, default='Nairobi')
    ppb_license = models.CharField(max_length=100, blank=True, default='')
    kra_pin = models.CharField(max_length=100, blank=True, default='')
    contact_person = models.CharField(max_length=150, blank=True, default='')
    contact_phone = models.CharField(max_length=50, blank=True, default='')
    date = models.DateField()
    due_date = models.DateField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    tax = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    grand_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=50, default='M-PESA')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.invoice_number} - {self.facility_name}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, blank=True, default='')
    batch_no = models.CharField(max_length=100, blank=True, default='')
    pack_size = models.CharField(max_length=100, blank=True, default='')
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name} x {self.quantity} on {self.invoice.invoice_number}"


class PaymentReceipt(models.Model):
    receipt_number = models.CharField(max_length=50, unique=True)
    invoice_number = models.CharField(max_length=50)
    facility_name = models.CharField(max_length=255)
    payment_method = models.CharField(max_length=50, default='M-PESA')
    reference_number = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    date = models.DateField()
    received_by = models.CharField(max_length=150, default='Omilife Treasury (Jared)')
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.receipt_number} - KES {self.amount}"


class OrderSalesNote(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='sales_notes')
    author = models.CharField(max_length=150, default='Sales Desk (Jared)')
    role = models.CharField(max_length=100, default='Admin')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.author} on Order {self.order.id}"


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    country_of_origin = models.CharField(max_length=100, default='India')
    contact_person = models.CharField(max_length=150, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    phone = models.CharField(max_length=50, blank=True, default='')
    ppb_gmp_cert = models.CharField(max_length=100, blank=True, default='PPB/GMP/FOREIGN/2024')
    lead_time_days = models.IntegerField(default=21)
    payment_terms = models.CharField(max_length=100, default='30% Advance, 70% against Bill of Lading')
    currency = models.CharField(max_length=10, default='USD')
    active_molecules = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.country_of_origin})"


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('SALE_DEDUCTION', 'Sale Deduction'),
        ('PURCHASE_INWARD', 'Purchase Inward'),
        ('DAMAGE_DISPOSAL', 'Damage Disposal'),
        ('PPB_AUDIT_SAMPLE', 'PPB Audit Sample'),
    ]

    sku = models.CharField(max_length=50)
    medicine_name = models.CharField(max_length=200)
    batch_number = models.CharField(max_length=100)
    movement_type = models.CharField(max_length=50, choices=MOVEMENT_TYPES, default='SALE_DEDUCTION')
    quantity = models.IntegerField()
    reference_number = models.CharField(max_length=100, blank=True, default='')
    balance_after = models.IntegerField(default=0)
    operator = models.CharField(max_length=100, default='System Auto-Deduction')
    notes = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type}: {self.medicine_name} ({self.quantity}) -> Bal {self.balance_after}"
