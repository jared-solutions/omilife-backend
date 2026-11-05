from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'hospitals', views.HospitalFacilityViewSet)
router.register(r'batches', views.ProductBatchViewSet)
router.register(r'suppliers', views.SupplierViewSet)
router.register(r'stock-movements', views.StockMovementViewSet)
router.register(r'invoices', views.InvoiceViewSet)
router.register(r'receipts', views.PaymentReceiptViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
