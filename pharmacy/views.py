from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import threading
import logging
from .models import (
    Product, Order, HospitalFacility, ProductBatch, 
    Invoice, PaymentReceipt, OrderSalesNote
)
from .serializers import (
    ProductSerializer, OrderSerializer, HospitalFacilitySerializer,
    ProductBatchSerializer, InvoiceSerializer, PaymentReceiptSerializer,
    OrderSalesNoteSerializer
)

logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Fetch all distinct product categories"""
        categories = Product.objects.values_list('category', flat=True).distinct()
        return Response(list(categories))

    
    @action(detail=True, methods=['post'])
    def add_note(self, request, pk=None):
        order = self.get_object()
        text = request.data.get('text', '')
        author = request.data.get('author', 'Sales Desk (Jared)')
        role = request.data.get('role', 'Admin')
        if not text:
            return Response({'error': 'Note text is required'}, status=status.HTTP_400_BAD_REQUEST)
        note = OrderSalesNote.objects.create(order=order, author=author, role=role, text=text)
        return Response(OrderSalesNoteSerializer(note).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        queryset = Product.objects.all()
        search = self.request.query_params.get('search', None)
        category = self.request.query_params.get('category', None)

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(active_ingredient__icontains=search)
            )

        if category and category != 'All':
            queryset = queryset.filter(category=category)

        return queryset

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all().order_by('-created_at')
        status_filter = self.request.query_params.get('status', None)

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

    def create(self, request, *args, **kwargs):
        logger.info("Received order data for creation.")

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error("Serializer errors during order creation: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        # Send emails: both admin notification and customer confirmation
        try:
            # 1. Admin notification email
            admin_subject = f'New Order Received - {order.pharmacy_name}'

            # Render HTML email template for admin
            admin_context = {
                'order': order,
                'static_url': 'https://omilife.co.ke/static/'
            }
            admin_html_message = render_to_string('pharmacy/email/order_confirmation.html', admin_context)

            # Plain text fallback for admin
            admin_plain_message = f"""
New order received from {order.pharmacy_name}

Order Details:
- Pharmacy: {order.pharmacy_name}
- Contact Person: {order.contact_person}
- Phone: {order.phone}
- Email: {order.email}
- County: {order.county}
- Town: {order.town}
- Address: {order.address}

Products Requested:
{order.products}

Additional Notes:
{order.message or 'None'}

Order ID: {order.id}
Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}

Please contact the customer within 2 hours to confirm the order.

--
Omilife Team
omilife.co.ke
"""

            # Send admin notification
            _send_mail_async(
                admin_subject,
                admin_plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                html_message=admin_html_message,
                fail_silently=True,
            )

            # 2. Customer confirmation email
            customer_subject = f'Order Confirmation - Omilife Pharmacy Order #{order.id}'

            # Create customer-specific email content
            customer_context = {
                'order': order,
                'is_customer_email': True,  # Flag to customize template for customers
                'static_url': 'https://omilife.co.ke/static/'
            }
            customer_html_message = render_to_string('pharmacy/email/order_confirmation.html', customer_context)

            customer_plain_message = f"""
Dear {order.contact_person},

Thank you for your order with Omilife! We have received your pharmacy order and our team will contact you shortly to confirm the details.

Order Details:
- Order ID: {order.id}
- Pharmacy: {order.pharmacy_name}
- Contact Person: {order.contact_person}
- Phone: {order.phone}
- Email: {order.email}
- County: {order.county}
- Town: {order.town}
- Address: {order.address}

Products Requested:
{order.products}

Additional Notes:
{order.message or 'None'}

Date: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}

Our sales team will contact you within 2 hours to confirm your order and arrange delivery.

For any questions, please contact us at:
- Phone: 0114976112 / 0723353615
- Email: sales@omilife.co.ke
- Website: https://omilife.co.ke

Thank you for choosing Omilife!

Best regards,
Omilife Team
"""

            # Send customer confirmation with automatic BCC to Admin (Option B)
            admin_bcc = [settings.ADMIN_EMAIL] if settings.ADMIN_EMAIL else None
            _send_mail_async(
                customer_subject,
                customer_plain_message,
                settings.ADMIN_EMAIL,  # Use sales@omilife.co.ke as from address
                [order.email],  # Send to customer's email
                html_message=customer_html_message,
                bcc=admin_bcc,  # Automatic copy to management
                fail_silently=True,
            )
        except Exception as e:
            # Record the error but still create the order
            logger.exception("Failed to send email notification")

        return Response(serializer.data, status=status.HTTP_201_CREATED)


def _send_mail_async(subject, message, from_email, recipient_list, html_message=None, bcc=None, fail_silently=True):
    """Send email in a background thread to avoid blocking the request."""
    def _worker():
        try:
            if html_message:
                # Use EmailMultiAlternatives for HTML emails with plain text alternative
                email = EmailMultiAlternatives(
                    subject=subject,
                    body=message,  # Plain text content
                    from_email=from_email,
                    to=recipient_list,
                    bcc=bcc,
                )
                # Attach HTML content
                email.attach_alternative(html_message, "text/html")
                email.send(fail_silently=fail_silently)
                logger.info("HTML email sent successfully (subject: %s)", subject)
            else:
                # Fallback to plain text
                result = send_mail(subject, message, from_email, recipient_list, fail_silently=fail_silently)
                logger.info("Email send result: %s (subject: %s)", result, subject)
                if result == 0:
                    logger.error("Email sending failed - no emails sent")
                else:
                    logger.info("Email sent successfully")
        except Exception as exc:
            logger.exception("Failed to send email asynchronously")

    threading.Thread(target=_worker, daemon=True).start()


class HospitalFacilityViewSet(viewsets.ModelViewSet):
    queryset = HospitalFacility.objects.all().order_by('-created_at')
    serializer_class = HospitalFacilitySerializer

class ProductBatchViewSet(viewsets.ModelViewSet):
    queryset = ProductBatch.objects.all().order_by('exp_date')
    serializer_class = ProductBatchSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all().order_by('-created_at')
    serializer_class = InvoiceSerializer

class PaymentReceiptViewSet(viewsets.ModelViewSet):
    queryset = PaymentReceipt.objects.all().order_by('-created_at')
    serializer_class = PaymentReceiptSerializer
