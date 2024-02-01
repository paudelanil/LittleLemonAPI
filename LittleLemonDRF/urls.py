from django.urls import path ,include
from . import views 
  
urlpatterns = [ 
    path('auth/', include('djoser.urls')), 
    path('auth/', include('djoser.urls.authtoken')), 
    # path('ratings', views.RatingsView.as_view()), 
    path('groups/managers/users',views.ManagerListView.as_view()),
    path('groups/managers/users/<int:pk>',views.ManagerRemoveView.as_view()),
    path('groups/managers/delivery-crew/users',views.DeliveryCrewListView.as_view()),
    path('groups/managers/delivery-crew/users/<int:pk>',views.DeliveryCrewRemoveView.as_view()),

    path('menu-items',views.MenuItemsView.as_view()),
    path('menu-items/<int:pk>',views.SingleMenuItemView.as_view()),

    path('cart/menu-items',views.CartDetailView.as_view()),
] 