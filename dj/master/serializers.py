# from .views import register
from rest_framework import serializers
from .models import Server
from django.contrib.auth import authenticate

# Add Money ////////////////////////////////////////////////////////////////////
from django.db.models import F
from django.db import transaction
from decimal import Decimal
# Add Money ////////////////////////////////////////////////////////////////////
class AddMoney(serializers.Serializer):
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    password = serializers.CharField(write_only=True)

    def validate_balance(self, value):
        if value < 50:
            raise serializers.ValidationError('balanceZero')
        elif value > 50000000000000000:
            raise serializers.ValidationError('balanceLimit')
        else:
            return value
    
    def validate_password(self, value):
        user = self.context.get('request').user
        
        if not user.check_password(value):
            raise serializers.ValidationError('passwordNotValid')
        else:
            return value
        
    def update(self, instance, validated_data):
        balance = validated_data['balance']
        
        try:
            with transaction.atomic():
                userLock = Server.objects.select_for_update().get(id=instance.id)

                userLock.balance = F('balance') + balance
                userLock.save(update_fields=['balance'])
                userLock.refresh_from_db()

                return userLock
        except:
            raise serializers.ValidationError({'error':'TransactionLoss'})
# Register ////////////////////////////////////////////////////////////////////
class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, value):
        already = Server.objects.filter(username=value)
        if already.exists():
            raise serializers.ValidationError('userAlready')
        elif len(value) < 8:
            raise serializers.ValidationError('usernameNotStrong')
        
        return value
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('passNotStrong')
        
        return value
    
    def create(self, validated_data):
        user = Server.objects.create_user(**validated_data)
        return user
# Login ///////////////////////////////////////////////////////////////////
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('userNotFound')
        else:
            refresh = RefreshToken.for_user(user)
            refresh['is_staff'] = user.is_staff

            attrs['user'] = user
            attrs['refresh_token'] = str(refresh)
            attrs['access_token'] = str(refresh.access_token)

            return attrs