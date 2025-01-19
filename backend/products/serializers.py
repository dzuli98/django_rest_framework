from rest_framework import serializers
from rest_framework.reverse import reverse
from api.serializers import UserPublicSerializer
from .models import Product
from .validators import validate_title, unique_product_title
'''
convert complex data type like model instance -> JSON
'''
class ProductSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    my_discount = serializers.SerializerMethodField(read_only=True) #this is a special field in Django REST Framework that allows you to define a custom method to calculate 
    url = serializers.SerializerMethodField(read_only=True)                                                              #the value of that field.
    class Meta:
        model = Product
        fields = [
            'user',
            'url',
            'pk',
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount'
        ]
    title = serializers.CharField(validators = [validate_title, unique_product_title])
    #email = serializers.EmailField(write_only=True)

    # def create(self, validated_data):
    #     email = validated_data.pop('email')
    #     obj = super().create(validated_data)
    #     print(email, obj)
    #     return obj

    #created validators module
    # def validate_title(self, value):
    #     request = self.context.get['request']
    #     user = request.user
    #     qs = Product.objects.filter(user=user, title__iexact=value)
    #     if qs.exists():
    #         raise serializers.ValidationError(f"{value} is already a product name")
    #     return value
    
    def get_url(self, obj):
        request = self.context.get('request')
        if reverse is None: 
            return None
        return reverse("product-detail", kwargs={'pk': obj.pk}, request=request)
    
    def get_my_discount(self, obj):
        if not isinstance(obj, Product):
            return None
        return obj.get_discount() # if error happens here (for example, obj is none)
