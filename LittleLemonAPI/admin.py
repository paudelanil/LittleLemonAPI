from django.contrib import admin
from .models import Rating,MenuItem,Category,Cart,Order

admin.site.register(Rating)
admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)