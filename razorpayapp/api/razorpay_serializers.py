from rest_framework import serializers
from ..models import Transaction


class RazorpayOrderSerializer(serializers.Serializer):
    amount = serializers.IntegerField()
    currency = serializers.CharField()


class TranscationModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ["payment_id", "order_id", "signature", "amount"]

class Allsbscibruserserializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ["payment_id", "order_id", "signature", "amount",'user_id']