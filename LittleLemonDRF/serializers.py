
from rest_framework import serializers 
from .models import (Rating ,MenuItem,Category,Cart,Order,OrderItem)
from rest_framework.validators import UniqueTogetherValidator 
from django.contrib.auth.models import User 
 

class RatingSerializer (serializers.ModelSerializer): 
    user = serializers.PrimaryKeyRelatedField( 
    queryset=User.objects.all(), 
    default=serializers.CurrentUserDefault() 
    ) 

    class Meta:
        model = Rating
        fields = ['user','menuitem_id','rating']

        validators = [UniqueTogetherValidator(queryset=Rating.objects.all(),fields =['user','menuitem_id','rating'])]
        extra_kwargs = {
            'rating':{'max_value':5,
                      'min_value':0,
                      },
        }
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']

class MenuItemSerializer(serializers.ModelSerializer):
    
    category = CategorySerializer()
    class Meta:
        model = MenuItem
        fields = ['title','price','featured','category']
        read_only_fields = ['category']

        
class ManagerListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields  = ['id','username','email']
class DeliverCrewListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id','username','email']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['username']
    
class MenuItemCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id','title','price']

class CartItemSerializer(serializers.ModelSerializer):

    # user = UserSerializer()
    menuitem  = MenuItemCartSerializer()
    class Meta:
        model = Cart
        fields = ['menuitem','quantity','price']

class CartAddItemSerializer(serializers.ModelSerializer):

    # user = UserSerializer()
    # menuitem  = MenuItemCartSerializer()
    class Meta:
        model = Cart
        fields = ['menuitem','quantity']
        extra_kwargs ={        
            'quantity':{'min_value':1},
        }

class CartRemoveSerializer(serializers.ModelSerializer):
    class Meta():
        model = Cart
        fields = ['menuitem']

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta():
        model = Order
        fields = ['id','user','total','status','delivery_crew','date']

class SingleHelperSerializer(serializers.ModelSerializer):
    class Meta():
        model = MenuItem
        fields = ['title','price']
class SingleOrderSerializer(serializers.ModelSerializer):
    menuitem = SingleHelperSerializer()
    class Meta():
        model = OrderItem
        fields = ['menuitem','quantity']


class OrderPutSerializer(serializers.ModelSerializer):
    class Meta():
        model = Order
        fields = ['delivery_crew']