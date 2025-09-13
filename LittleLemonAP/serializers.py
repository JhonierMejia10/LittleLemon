from rest_framework import serializers
from .models import MenuItem, Category
import bleach

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'





class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    #def validate_title(self, value):
    #   return bleach.clean(value)

    def validate(self, attrs):
         attrs['title'] = bleach.clean(attrs['title'])
         if(attrs['price']<2):
             raise serializers.ValidationError('Price should not be less than 2.0')
         if(attrs['inventory']<0):
             raise serializers.ValidationError('Stock cannot be negative')
         return super().validate(attrs)

    class Meta:
        model = MenuItem
        fields = ['id','title','price','inventory','category']

    def create(self, validate_data):
        category_data = validate_data.pop('category')
        category, created = Category.objects.get_or_create(**category_data)
        menu_item = MenuItem.objects.create(category=category, **validate_data)
        return menu_item



