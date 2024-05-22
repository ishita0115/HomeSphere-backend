from django.urls import path
from .api_razorpay import PaymentStatusView, RazorpayOrderAPIView, TransactionAPIView

urlpatterns = [
    path("order/create/", 
        RazorpayOrderAPIView.as_view(), 
        name="razorpay-create-order-api"
    ),
    path("order/complete/", 
        TransactionAPIView.as_view(), 
        name="razorpay-complete-order-api"
    ),
    path('payment-status/<str:uid>/', PaymentStatusView.as_view()),
]