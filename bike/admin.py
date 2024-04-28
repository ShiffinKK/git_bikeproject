from django.contrib import admin
from bike.models import Category,Bike,Service,PriceRange,Order

admin.site.register(Category)
admin.site.register(Bike)
admin.site.register(Service)
admin.site.register(PriceRange)
admin.site.register(Order)

# Register your models here.
