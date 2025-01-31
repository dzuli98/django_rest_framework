from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Product

# if you have validators on the model
# we dont have to worry about this
# usually put validators on the model
# but sometimes validators are needed inside serializers
# because of request context

def validate_title(value):
    qs = Product.objects.filter(title__iexact=value)
    if qs.exists():
        raise serializers.ValidationError(f"{value} is already a product name")
    return value

unique_product_title = UniqueValidator(queryset=Product.objects.all(), lookup='iexact')