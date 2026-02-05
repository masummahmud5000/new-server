# from .views import register
from rest_framework import serializers
from .models import Server
from django.contrib.auth import authenticate

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
            return {'user': user}