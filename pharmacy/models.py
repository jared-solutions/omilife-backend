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
