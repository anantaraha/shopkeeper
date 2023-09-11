from django.contrib import admin
from . import models

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'label',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'brand', 'unit', 'price', 'quantity', 'enabled', 'available',)


class ProductSaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'quantity', 'bill_id',)


class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'time', 'total', 'display_items',)


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductSale, ProductSaleAdmin)
admin.site.register(models.Bill, BillAdmin)