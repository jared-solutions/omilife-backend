import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'omilife_backend.settings')
django.setup()

from pharmacy.models import (
    Product, HospitalFacility, ProductBatch, Invoice, InvoiceItem, PaymentReceipt, Order, OrderSalesNote
)
from datetime import date

print("Seeding Omilife ERP Data into Database...")

# 1. Seed Partner Hospitals
hospitals_data = [
    {
        'name': 'Aga Khan University Hospital',
        'facility_type': 'Teaching/Referral Hospital',
        'county': 'Nairobi',
        'address': '3rd Parklands Ave, Nairobi',
        'ppb_license': 'PPB/PREM/NRB/4401',
        'kra_pin': 'P051299881K',
        'contact_person': 'Dr. Caroline Mwangi (Chief Pharmacist)',
        'phone': '+254 722 100 200',
        'email': 'pharmacy.procurement@aku.edu',
        'credit_limit': 2500000.00,
        'outstanding_balance': 469500.00,
        'tier': 'Platinum Partner'
    },
    {
        'name': 'The Nairobi Hospital',
        'facility_type': 'Private Level 5',
        'county': 'Nairobi',
        'address': 'Argwings Kodhek Rd, Nairobi',
        'ppb_license': 'PPB/PREM/NRB/1029',
        'kra_pin': 'P051011244A',
        'contact_person': 'Pharm. David Oloo',
        'phone': '+254 733 450 120',
        'email': 'medsupplies@nairobihospital.org',
        'credit_limit': 3000000.00,
        'outstanding_balance': 401500.00,
        'tier': 'Platinum Partner'
    },
    {
        'name': 'Avenue Healthcare Parklands',
        'facility_type': 'Private Level 5',
        'county': 'Nairobi',
        'address': 'Parklands Road, Nairobi',
        'ppb_license': 'PPB/PREM/NRB/8821',
        'kra_pin': 'P051882110B',
        'contact_person': 'Dr. Peter Gitonga',
        'phone': '+254 711 900 340',
        'email': 'procure@avenuehealthcare.com',
        'credit_limit': 1500000.00,
        'outstanding_balance': 215000.00,
        'tier': 'Platinum Partner'
    },
    {
        'name': 'Kisumu Specialists Hospital',
        'facility_type': 'Private Level 5',
        'county': 'Kisumu',
        'address': 'Mega City Complex, Kisumu',
        'ppb_license': 'PPB/PREM/KSM/0512',
        'kra_pin': 'P051930211L',
        'contact_person': 'Pharm. Grace Akoth',
        'phone': '+254 720 891 140',
        'email': 'dispensary@kisumuspecialists.ke',
        'credit_limit': 1000000.00,
        'outstanding_balance': 0.00,
        'tier': 'Standard Hospital'
    },
    {
        'name': 'Mombasa Hospital',
        'facility_type': 'Private Level 5',
        'county': 'Mombasa',
        'address': 'School Lane, Kizingo, Mombasa',
        'ppb_license': 'PPB/PREM/MSA/2219',
        'kra_pin': 'P051772199C',
        'contact_person': 'Dr. Salim Abdalla',
        'phone': '+254 733 902 110',
        'email': 'pharmacy@mombasahospital.com',
        'credit_limit': 1200000.00,
        'outstanding_balance': 0.00,
        'tier': 'Standard Hospital'
    },
    {
        'name': 'Goodlife Pharmacy Junction Mall',
        'facility_type': 'Retail Pharmacy Chain',
        'county': 'Nairobi',
        'address': 'Ngong Road, Nairobi',
        'ppb_license': 'PPB/RET/NRB/9011',
        'kra_pin': 'P051009188M',
        'contact_person': 'Pharm. Edwin Kiprotich',
        'phone': '+254 719 555 432',
        'email': 'junction@goodlife.co.ke',
        'credit_limit': 800000.00,
        'outstanding_balance': 0.00,
        'tier': 'Retail Chemist'
    }
]

for hd in hospitals_data:
    HospitalFacility.objects.update_or_create(
        name=hd['name'],
        defaults=hd
    )
print(f"Hospitals seeded: {len(hospitals_data)}")

# 2. Seed Warehouse Batches
batches_data = [
    {'sku': 'OMI-TUM-10', 'medicine_name': 'Tumivono 10mg', 'strength': '10mg', 'batch_number': 'TUM-2025-08', 'mfg_date': date(2024, 9, 1), 'exp_date': date(2027, 8, 31), 'quantity_packs': 340, 'warehouse_location': 'Aisle 3 - Shelf B (Ambient <25°C)', 'unit_cost_kes': 1100.00, 'selling_price_kes': 1650.00},
    {'sku': 'OMI-TUM-20', 'medicine_name': 'Tumivono 20mg', 'strength': '20mg', 'batch_number': 'TUM-2025-11', 'mfg_date': date(2024, 11, 1), 'exp_date': date(2027, 10, 15), 'quantity_packs': 285, 'warehouse_location': 'Aisle 3 - Shelf C (Ambient <25°C)', 'unit_cost_kes': 1650.00, 'selling_price_kes': 2450.00},
    {'sku': 'OMI-ALQ-25', 'medicine_name': 'Aliqa 2.5mg', 'strength': '2.5mg', 'batch_number': 'ALQ-2025-04', 'mfg_date': date(2024, 1, 15), 'exp_date': date(2026, 12, 30), 'quantity_packs': 190, 'warehouse_location': 'Cold-Vault 1 (15-25°C Monitored)', 'unit_cost_kes': 2600.00, 'selling_price_kes': 3800.00},
    {'sku': 'OMI-ALQ-50', 'medicine_name': 'Aliqa 5mg', 'strength': '5mg', 'batch_number': 'ALQ-2025-09', 'mfg_date': date(2024, 5, 10), 'exp_date': date(2027, 4, 12), 'quantity_packs': 420, 'warehouse_location': 'Cold-Vault 1 (15-25°C Monitored)', 'unit_cost_kes': 3300.00, 'selling_price_kes': 4950.00},
    {'sku': 'OMI-DNT-800', 'medicine_name': 'Donet 800 SR', 'strength': '800mg', 'batch_number': 'DNT-2025-02', 'mfg_date': date(2024, 3, 1), 'exp_date': date(2026, 11, 20), 'quantity_packs': 110, 'warehouse_location': 'Aisle 4 - Shelf A', 'unit_cost_kes': 4200.00, 'selling_price_kes': 6200.00},
    {'sku': 'OMI-DNM-400', 'medicine_name': 'Donet-M 400 SR', 'strength': '400mg + 300mg', 'batch_number': 'DNM-2025-06', 'mfg_date': date(2024, 6, 15), 'exp_date': date(2027, 1, 18), 'quantity_packs': 145, 'warehouse_location': 'Aisle 4 - Shelf B', 'unit_cost_kes': 3500.00, 'selling_price_kes': 5100.00},
    {'sku': 'OMI-DNM-800', 'medicine_name': 'Donet-M 800 SR', 'strength': '800mg + 600mg', 'batch_number': 'DNM-2025-07', 'mfg_date': date(2024, 7, 20), 'exp_date': date(2027, 2, 28), 'quantity_packs': 95, 'warehouse_location': 'Aisle 4 - Shelf C', 'unit_cost_kes': 5400.00, 'selling_price_kes': 7800.00},
    {'sku': 'OMI-TFL-01', 'medicine_name': 'Tumiflo 1mg', 'strength': '1mg', 'batch_number': 'TFL-2025-03', 'mfg_date': date(2024, 4, 1), 'exp_date': date(2026, 9, 30), 'quantity_packs': 310, 'warehouse_location': 'Aisle 2 - Shelf A', 'unit_cost_kes': 1250.00, 'selling_price_kes': 1850.00},
    {'sku': 'OMI-TFL-02', 'medicine_name': 'Tumiflo 2mg', 'strength': '2mg', 'batch_number': 'TFL-2025-05', 'mfg_date': date(2024, 5, 18), 'exp_date': date(2026, 10, 15), 'quantity_packs': 260, 'warehouse_location': 'Aisle 2 - Shelf B', 'unit_cost_kes': 1800.00, 'selling_price_kes': 2600.00},
    {'sku': 'OMI-PLD-03', 'medicine_name': 'Palido 3mg', 'strength': '3mg', 'batch_number': 'PLD-2025-01', 'mfg_date': date(2024, 2, 10), 'exp_date': date(2026, 8, 14), 'quantity_packs': 75, 'warehouse_location': 'Secure Vault C', 'unit_cost_kes': 2900.00, 'selling_price_kes': 4200.00},
    {'sku': 'OMI-PLD-06', 'medicine_name': 'Palido 6mg', 'strength': '6mg', 'batch_number': 'PLD-2025-03', 'mfg_date': date(2024, 3, 25), 'exp_date': date(2026, 9, 1), 'quantity_packs': 60, 'warehouse_location': 'Secure Vault C', 'unit_cost_kes': 4100.00, 'selling_price_kes': 5900.00},
    {'sku': 'OMI-RTR-05', 'medicine_name': 'Ritri 5mg', 'strength': '5mg', 'batch_number': 'RTR-2025-04', 'mfg_date': date(2024, 4, 10), 'exp_date': date(2027, 5, 19), 'quantity_packs': 230, 'warehouse_location': 'Aisle 5 - Cold Vault', 'unit_cost_kes': 2300.00, 'selling_price_kes': 3400.00},
    {'sku': 'OMI-RTR-10', 'medicine_name': 'Ritri 10mg', 'strength': '10mg', 'batch_number': 'RTR-2025-06', 'mfg_date': date(2024, 6, 1), 'exp_date': date(2027, 6, 30), 'quantity_packs': 180, 'warehouse_location': 'Aisle 5 - Cold Vault', 'unit_cost_kes': 3100.00, 'selling_price_kes': 4600.00},
]

for bd in batches_data:
    ProductBatch.objects.update_or_create(
        batch_number=bd['batch_number'],
        defaults=bd
    )
print(f"Batches seeded: {len(batches_data)}")

# 3. Seed Invoices & Items
invoices_data = [
    {
        'invoice_number': 'OMI-INV-2026-0142',
        'facility_name': 'Aga Khan University Hospital',
        'facility_type': 'Teaching/Referral Hospital',
        'county': 'Nairobi',
        'ppb_license': 'PPB/PREM/NRB/4401',
        'kra_pin': 'P051299881K',
        'contact_person': 'Dr. Caroline Mwangi',
        'contact_phone': '+254 722 100 200',
        'date': date(2026, 11, 1),
        'due_date': date(2026, 11, 30),
        'subtotal': 469500.00,
        'tax': 0.00,
        'grand_total': 469500.00,
        'payment_method': 'CREDIT_30_DAYS',
        'payment_status': 'PENDING',
        'amount_paid': 0.00,
        'notes': 'Prescription pharmaceuticals zero-rated per KRA First Schedule Section B. Cold-chain storage maintained below 25°C.',
        'items': [
            {'name': 'Aliqa 5mg (Apixaban)', 'sku': 'OMI-ALQ-50', 'batch_no': 'ALQ-2025-09', 'pack_size': '30s Blister', 'quantity': 50, 'unit_price': 4950.00, 'total': 247500.00},
            {'name': 'Tumivono 20mg (Vonoprazan)', 'sku': 'OMI-TUM-20', 'batch_no': 'TUM-2025-11', 'pack_size': '10x10 Box', 'quantity': 40, 'unit_price': 2450.00, 'total': 98000.00},
            {'name': 'Donet 800 SR (Pirfenidone)', 'sku': 'OMI-DNT-800', 'batch_no': 'DNT-2025-02', 'pack_size': '30s Bottle', 'quantity': 20, 'unit_price': 6200.00, 'total': 124000.00},
        ]
    },
    {
        'invoice_number': 'OMI-INV-2026-0141',
        'facility_name': 'Kisumu Specialists Hospital',
        'facility_type': 'Private Level 5',
        'county': 'Kisumu',
        'ppb_license': 'PPB/PREM/KSM/0512',
        'kra_pin': 'P051930211L',
        'contact_person': 'Pharm. Grace Akoth',
        'contact_phone': '+254 720 891 140',
        'date': date(2026, 10, 29),
        'due_date': date(2026, 10, 29),
        'subtotal': 193000.00,
        'tax': 0.00,
        'grand_total': 193000.00,
        'payment_method': 'BANK_RTGS',
        'payment_status': 'PAID',
        'amount_paid': 193000.00,
        'notes': 'Dispatched via G4S Secure Courier Kisumu Branch. Transit temperature logger attached.',
        'items': [
            {'name': 'Tumiflo 2mg (Silodosin)', 'sku': 'OMI-TFL-02', 'batch_no': 'TFL-2025-05', 'pack_size': '30s Capsules', 'quantity': 30, 'unit_price': 2600.00, 'total': 78000.00},
            {'name': 'Ritri 10mg (Rivaroxaban)', 'sku': 'OMI-RTR-10', 'batch_no': 'RTR-2025-06', 'pack_size': '28s Tablets', 'quantity': 25, 'unit_price': 4600.00, 'total': 115000.00},
        ]
    },
    {
        'invoice_number': 'OMI-INV-2026-0140',
        'facility_name': 'Goodlife Pharmacy Junction Mall',
        'facility_type': 'Retail Pharmacy Chain',
        'county': 'Nairobi',
        'ppb_license': 'PPB/RET/NRB/9011',
        'kra_pin': 'P051009188M',
        'contact_person': 'Pharm. Edwin Kiprotich',
        'contact_phone': '+254 719 555 432',
        'date': date(2026, 10, 28),
        'due_date': date(2026, 10, 28),
        'subtotal': 90000.00,
        'tax': 0.00,
        'grand_total': 90000.00,
        'payment_method': 'M-PESA',
        'payment_status': 'PAID',
        'amount_paid': 90000.00,
        'notes': 'Counter Walk-in Direct Requisition settled via M-Pesa Buy Goods.',
        'items': [
            {'name': 'Tumivono 10mg', 'sku': 'OMI-TUM-10', 'batch_no': 'TUM-2025-08', 'pack_size': '10x10 Box', 'quantity': 20, 'unit_price': 1650.00, 'total': 33000.00},
            {'name': 'Aliqa 2.5mg', 'sku': 'OMI-ALQ-25', 'batch_no': 'ALQ-2025-04', 'pack_size': '30s Blister', 'quantity': 15, 'unit_price': 3800.00, 'total': 57000.00},
        ]
    }
]

for inv_data in invoices_data:
    items = inv_data.pop('items')
    inv, created = Invoice.objects.update_or_create(
        invoice_number=inv_data['invoice_number'],
        defaults=inv_data
    )
    inv.items.all().delete()
    for it in items:
        InvoiceItem.objects.create(invoice=inv, **it)

print(f"Invoices seeded: {len(invoices_data)}")

# 4. Seed Payment Receipts
receipts_data = [
    {
        'receipt_number': 'OMI-REC-2026-0089',
        'invoice_number': 'OMI-INV-2026-0141',
        'facility_name': 'Kisumu Specialists Hospital',
        'payment_method': 'BANK_RTGS',
        'reference_number': 'RTGS-KCB-994102931',
        'amount': 193000.00,
        'date': date(2026, 10, 29),
        'received_by': 'Jared (Omilife Accounts)',
        'notes': 'Payment confirmed via KCB Bank Kenya Treasury portal.'
    },
    {
        'receipt_number': 'OMI-REC-2026-0088',
        'invoice_number': 'OMI-INV-2026-0140',
        'facility_name': 'Goodlife Pharmacy Junction Mall',
        'payment_method': 'M-PESA',
        'reference_number': 'SLK992XQ10',
        'amount': 90000.00,
        'date': date(2026, 10, 28),
        'received_by': 'Omilife Direct Sales Counter',
        'notes': 'M-Pesa Business Till receipt verified.'
    }
]

for rd in receipts_data:
    PaymentReceipt.objects.update_or_create(
        receipt_number=rd['receipt_number'],
        defaults=rd
    )
print(f"Receipts seeded: {len(receipts_data)}")
print("Seeding Completed Successfully!")
