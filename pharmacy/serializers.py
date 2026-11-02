from rest_framework import serializers
from .models import Product, ProductImage, Order

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image_url', 'is_main']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'category', 'price', 'unit', 'in_stock', 'bonus',
            'active_ingredient', 'strength', 'manufacturer', 'indication', 'dosage',
            'side_effects', 'contraindications', 'storage_requirements', 'batch_info',
            'expiry_info', 'images', 'created_at', 'updated_at'
        ]

class OrderSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        # Allow products to be sent as list, dict or string
        if isinstance(data, dict) and 'products' in data:
            raw_products = data.get('products')
            if isinstance(raw_products, list):
                lines = []
                for item in raw_products:
                    if isinstance(item, dict):
                        name = item.get('name', 'Item')
                        qty = item.get('quantity', 1)
                        lines.append(f"• {name} (Qty: {qty})")
                    else:
                        lines.append(f"• {str(item)}")
                data = data.copy()
                data['products'] = "\n".join(lines)
        return super().to_internal_value(data)

    class Meta:
        model = Order
        fields = [
            'id', 'pharmacy_name', 'contact_person', 'phone', 'email',
            'county', 'town', 'address', 'products', 'message', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']
