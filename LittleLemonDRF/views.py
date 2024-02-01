from rest_framework import generics
from django.shortcuts import get_object_or_404
from .models import ( Rating,MenuItem,OrderItem,Order,Category,Cart)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, JsonResponse
from django.contrib.auth.models import User,Group
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .serializers import (
   
    MenuItemSerializer,
    CategorySerializer,
    RatingSerializer,
    ManagerListSerializer,
    DeliverCrewListSerializer,
    CartItemSerializer,
    CartAddItemSerializer,
    CartRemoveSerializer,
   
)
from .permissions import (
  
    IsManager,
    IsDeliveryCrew,
    
)
class RatingsView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permission(self):
        if(self.request.method =='GET'):
            return[]
        return [IsAuthenticated()]

        
class MenuItemsView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['title', 'price', 'featured']
    search_fields = ['title', 'price', 'featured']
    filterset_fields = ['title', 'price', 'featured']

    def get_permissions(self):
        permission_classes = []
        if self.request.method != 'GET':
                permission_classes = [IsAuthenticated, IsAdminUser]
        return[permission() for permission in permission_classes]
    
    

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    model = MenuItem
    queryset = model.objects.all()
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        if self.request.method == 'PATCH':
            permission_classes = [IsAuthenticated, IsManager | IsAdminUser]
        if self.request.method == "DELETE":
            permission_classes = [IsAuthenticated, IsAdminUser]
        return[permission() for permission in permission_classes]

    def patch(self, request, *args, **kwargs):
        menuitem = MenuItem.objects.get(pk=self.kwargs['pk'])
        menuitem.featured = not menuitem.featured
        menuitem.save()
        return JsonResponse(status=200, data={'message':'Featured status of {} changed to {}'.format(str(menuitem.title) ,str(menuitem.featured))})
        
class ManagerListView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name = 'Manager')
    serializer_class = ManagerListSerializer
    permission_classes = [IsAuthenticated, IsManager | IsAdminUser]

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name='Manager')
            managers.user_set.add(user)
            return JsonResponse(status=201, data={'message':'User added to Managers group'}) 

class ManagerRemoveView(generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name = 'Manager')
    serializer_class = ManagerListSerializer
    permission_classes = [IsAuthenticated, IsManager | IsAdminUser ]

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        user = get_object_or_404(User,pk = pk)
        manager = Group.objects.get(name = 'Manager')
        manager.user_set.remove(user)
        return JsonResponse(status = 200,data ={'message':'User removed Manager group'})
        return super().delete(request, *args, **kwargs)
    
class DeliveryCrewListView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name = 'Delivery Crew')
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    serializer_class = DeliverCrewListSerializer
    permission_classes = [IsAuthenticated, IsManager | IsAdminUser]

    def post(self, request, *args, **kwargs):
        username = request.data['username']
        if username:
            user = get_object_or_404(User, username=username)
            managers = Group.objects.get(name='Delivery Crew')
            managers.user_set.add(user)

class DeliveryCrewRemoveView(generics.DestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name = 'Delivery Crew')
    serializer_class = DeliverCrewListSerializer
    permission_classes = [IsAuthenticated, IsManager | IsAdminUser ]

    def delete(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        user = get_object_or_404(User,pk = pk)
        manager = Group.objects.get(name = 'Delivery Crew')
        manager.user_set.remove(user)
        return JsonResponse(status = 200,data ={'message':'User removed Delivery group'})
        
class CartDetailView(generics.ListCreateAPIView,generics.DestroyAPIView):
    throttle_classes = [ AnonRateThrottle,UserRateThrottle]
    queryset = Cart.objects.all()
    serializer_class = CartItemSerializer

    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        cart = Cart.objects.filter(user= self.request.user)
        return cart
    def post(self, request, *args, **kwargs):
        serialized_item = CartAddItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        id = request.data['menuitem']
        quantity = request.data['quantity']
        item = get_object_or_404(MenuItem,id = id)
        total_price = int(quantity) * item.price

        try:
            Cart.objects.create(user=request.user, quantity=quantity, unit_price=item.price, price=total_price, menuitem_id=id)
        except:
            return JsonResponse(status=409, data={'message':'Item already in cart'})
        return JsonResponse(status=201, data={'message':'Item added to cart!'})

    def delete(self, request, *arg, **kwargs):
        if request.data['menuitem']:
            serialized_item = CartRemoveSerializer(data=request.data)
            serialized_item.is_valid(raise_exception=True)
            menuitem = request.data['menuitem']
            cart = get_object_or_404(Cart, user=request.user, menuitem=menuitem )
            cart.delete()
            return JsonResponse(status=200, data={'message':'Item removed from cart'})
        else:
            Cart.objects.filter(user=request.user).delete()
            return JsonResponse(status=201, data={'message':'All Items removed from cart'})

