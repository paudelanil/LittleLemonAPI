from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Rating,MenuItem
from .serializers import RatingSerializer,MenuItemSerializer

class RatingsView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permission(self):
        if(self.request.method =='GET'):
            return[]
        return [IsAuthenticated()]

        
class MenuItemsView(generics.ListCreateAPIView):

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer