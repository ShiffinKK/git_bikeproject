from rest_framework import serializers
from bike.models import Bike,Wishlist,WishlistItem,Service,Order
from django.contrib.auth. models import User

class UserSerializer(serializers.ModelSerializer):
    password1=serializers.CharField(write_only=True)
    password2=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=["id","username","email","password1","password2","password"]
        read_only_fields=["id","password"]

    def create(self, validated_data):
        password1=validated_data.pop("password1")
        password2=validated_data.pop("password2")
        if password1!=password2:
            raise serializers.ValidationError("password missmatch")
        return User.objects.create_user(**validated_data,password=password1)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bike
        fields="__all__"

class CompareBikeObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bike
        fields=["title","price","image"]

class CompareItemSerializer(serializers.ModelSerializer):
    
    Bike_object=CompareBikeObjectSerializer(read_only=True)
    class Meta:
        model=Wishlist
        fields=[
            "id",
            "Bike_object",
            
            

        ]

class CompareSerializer(serializers.ModelSerializer):
    owner=serializers.StringRelatedField()
    wish_item=CompareItemSerializer(many=True)
    recoment=serializers.CharField()
    class Meta:
        model=WishlistItem
        fields=[
            "id",
            "owner",
            "wish_item",
            "recoment"
        ]

class ServiceSerializer(serializers.ModelSerializer):
    owner=serializers.StringRelatedField()

    class Meta:
        model=Service
        fields="__all__"




class OrderSerializer(serializers.ModelSerializer):
        Bike_object=ProductSerializer(read_only=True)

        class Meta:
           model=Order
           fields="__all__"
    