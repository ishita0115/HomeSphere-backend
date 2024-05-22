from rest_framework.views import APIView
from rest_framework import status

from app1.models import User
from razorpayapp.models import Transaction
from .razorpay_serializers import Allsbscibruserserializer, RazorpayOrderSerializer, TranscationModelSerializer
from razorpayapp.api.razorpay.main import RazorpayClient
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
rz_client = RazorpayClient()

class RazorpayOrderAPIView(APIView):
    """This API will create an order"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        razorpay_order_serializer = RazorpayOrderSerializer(
            data=request.data
        )
        if razorpay_order_serializer.is_valid():
            order_response = rz_client.create_order(
                amount=razorpay_order_serializer.validated_data.get("amount"),
                currency=razorpay_order_serializer.validated_data.get("currency")
            )
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "order created",
                "data": order_response
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": razorpay_order_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class TransactionAPIView(APIView):
    """This API will complete order and save the 
    transaction"""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        print(request.user)
        transaction_serializer = TranscationModelSerializer(data=request.data)
        if transaction_serializer.is_valid():
            rz_client.verify_payment_signature(
                razorpay_payment_id = transaction_serializer.validated_data.get("payment_id"),
                razorpay_order_id = transaction_serializer.validated_data.get("order_id"),
                razorpay_signature = transaction_serializer.validated_data.get("signature")
            )
            transaction_serializer.save(user=request.user,status="Done")
            response = {
                "status_code": status.HTTP_201_CREATED,
                "message": "transaction successfully create"
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": "bad request",
                "error": transaction_serializer.errors
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        

class PaymentStatusView(APIView):

    def get(self, request, uid):
        try:
            user_transactions = Transaction.objects.filter(user__uid=uid)
            if user_transactions.exists():
                # Check if any of the user's transactions have status 'Done'
                if user_transactions.filter(status='Done').exists():
                    return Response({'payment_done': True}, status=status.HTTP_200_OK)
            
            # If no transactions exist for the user or none of them have status 'Done', return False
            return Response({'payment_done': False}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class Allsubscribeuser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user_ids = Transaction.objects.values_list('user_id', flat=True).distinct()
        
        # Return the list of distinct user IDs
        users = User.objects.filter(id__in=user_ids)
        
        # Serialize user data if needed
        user_data = [{"id": user.id, "Firstname": user.first_name,'lastname':user.last_name,'email':user.email} for user in users]
        
        # Return the user data as response
        return Response(user_data, status=status.HTTP_200_OK)