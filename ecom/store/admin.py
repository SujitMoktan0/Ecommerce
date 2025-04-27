from django.contrib import admin
from .models import Customer, Product, Category, Order
from django.db.models import TextField
from django.forms import Textarea
from rangefilter.filters import DateRangeFilter  # For date range filtering

class ProductAdmin(admin.ModelAdmin):
    # Product-specific search and filters
    search_fields = ['name', 'description', 'category__name', 'seller__username']
    list_filter = [
        'category',
        'has_discount',
        ('date', DateRangeFilter),  # Date range filter
        'seller'
    ]
    # ... rest of your ProductAdmin ...

class CustomerAdmin(admin.ModelAdmin):
    # Customer-specific search and filters
    search_fields = ['first_name', 'last_name', 'email', 'phone']
    list_filter = [
        ('date', DateRangeFilter),  # Date range filter
    ]
    # ... rest of your CustomerAdmin ...

class OrderAdmin(admin.ModelAdmin):
    # Order-specific search and filters
    search_fields = [
        'product__name',
        'customer__first_name',
        'customer__last_name',
        'customer__email'
    ]
    list_filter = [
        'status',
        ('date', DateRangeFilter),  # Date range filter
        'product__category'
    ]
    # ... rest of your OrderAdmin ...

class CategoryAdmin(admin.ModelAdmin):
    # Category-specific search
    search_fields = ['name']
    # ... rest of your CategoryAdmin ...

# Register your models
admin.site.register(Category, CategoryAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)

from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter
)

class ProductAdmin(admin.ModelAdmin):
    list_filter = [
        ('category', RelatedDropdownFilter),  # Dropdown for categories
        ('price', DropdownFilter),  # Dropdown for price ranges
        ('date', DateRangeFilter),
        'has_discount',
        ('seller', RelatedDropdownFilter),
    ]