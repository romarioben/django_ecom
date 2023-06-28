from django.contrib import admin
from django.urls import reverse
from . import models
from django.utils.html import format_html

# Register your models here.
@admin.register(models.Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']


@admin.register(models.Customer)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'state', 'zipcode']

@admin.register(models.Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']
    def product(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}<a>', link, obj.product.title)

@admin.register(models.Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'razorpay_order_id', 'razorpay_payment_status', 'razorpay_payment_id', 'paid']


@admin.register(models.OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer', 'product', 'quantity', 'ordered_date', 'status', 'payment']

@admin.register(models.Wishlist)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product']