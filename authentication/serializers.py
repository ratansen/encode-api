from rest_framework import serializers
from authentication.models import NewUser


class TokenSerializer(serializers.Serializer):
    """
    This serializer serializes the token data
    """
    token = serializers.CharField(max_length=255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = "__all__" 
