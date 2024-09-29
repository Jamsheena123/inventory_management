from rest_framework import serializers
# from .models import CustomUser, Item
from .models import User, Item







class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']  
        extra_kwargs = {'password': {'write_only': True}}

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'added_by', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at'] 

    
