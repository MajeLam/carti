from rest_framework import serializers
from .models import User, BankAccount, CreditCard, CardTransaction

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'address', 'date_of_birth', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class BankAccountSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = BankAccount
        fields = ('id', 'account_number', 'owner', 'balance', 'currency', 'created_at', 'updated_at')

class CreditCardSerializer(serializers.ModelSerializer):
    account = BankAccountSerializer(read_only=True)
    
    class Meta:
        model = CreditCard
        fields = ('id', 'card_number', 'expiration_date', 'cvv', 'account', 'card_type', 
                 'is_active', 'daily_limit', 'monthly_limit', 'created_at', 'updated_at')
        extra_kwargs = {'cvv': {'write_only': True}}

class CardTransactionSerializer(serializers.ModelSerializer):
    card = CreditCardSerializer(read_only=True)
    
    class Meta:
        model = CardTransaction
        fields = ('id', 'card', 'amount', 'transaction_type', 'merchant_name', 
                 'transaction_date', 'status', 'description')

class VirtualCardRequestSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=20)
    daily_limit = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    monthly_limit = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)