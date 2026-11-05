from rest_framework import serializers
from .models import (
    Product, ProductImage, Order, HospitalFacility, 
    ProductBatch, Invoice, InvoiceItem, PaymentReceipt, OrderSalesNote,
    Supplier, StockMovement
)

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

class OrderSalesNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderSalesNote
        fields = ['id', 'author', 'role', 'text', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    sales_notes = OrderSalesNoteSerializer(many=True, read_only=True)

    def to_internal_value(self, data):
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
            'sales_notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class HospitalFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalFacility
        fields = '__all__'

class ProductBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductBatch
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = '__all__'

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'name', 'sku', 'batch_no', 'pack_size', 'quantity', 'unit_price', 'total']

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, required=False)

    class Meta:
        model = Invoice
        fields = [
            'id', 'invoice_number', 'order', 'facility_name', 'facility_type',
            'county', 'ppb_license', 'kra_pin', 'contact_person', 'contact_phone',
            'date', 'due_date', 'subtotal', 'tax', 'grand_total', 'payment_method',
            'payment_status', 'amount_paid', 'notes', 'items', 'created_at'
        ]

    def create(self, validated_data):
        items_data = self.initial_data.get('items', [])
        invoice = Invoice.objects.create(**validated_data)
        
        for it in items_data:
            qty_sold = int(it.get('quantity', 1))
            batch_num = it.get('batchNo', it.get('batch_no', ''))
            sku_code = it.get('sku', '')

            InvoiceItem.objects.create(
                invoice=invoice,
                name=it.get('name', 'Prescription Medication'),
                sku=sku_code,
                batch_no=batch_num,
                pack_size=it.get('packSize', it.get('pack_size', '')),
                quantity=qty_sold,
                unit_price=float(it.get('unitPrice', it.get('unit_price', 0))),
                total=float(it.get('total', 0))
            )

            # Real-time automatic inventory deduction
            batch = None
            if batch_num:
                batch = ProductBatch.objects.filter(batch_number=batch_num).first()
            elif sku_code:
                batch = ProductBatch.objects.filter(sku=sku_code).first()

            if batch:
                new_qty = max(0, batch.quantity_packs - qty_sold)
                batch.quantity_packs = new_qty
                batch.save()

                StockMovement.objects.create(
                    sku=batch.sku,
                    medicine_name=batch.medicine_name,
                    batch_number=batch.batch_number,
                    movement_type='SALE_DEDUCTION',
                    quantity=-qty_sold,
                    reference_number=invoice.invoice_number,
                    balance_after=new_qty,
                    operator='Direct Sales Counter',
                    notes=f"Auto-deducted {qty_sold} pack(s) for Invoice {invoice.invoice_number} ({invoice.facility_name})"
                )

        return invoice

class PaymentReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentReceipt
        fields = '__all__'
