from rest_framework import serializers
from .models import MenuItem, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = MenuItem
        fields = ['id','title','price','inventory','category']

    def create(self, validate_data):
        category_data = validate_data.pop('category')
        category, created = Category.objects.get_or_create(**category_data)
        menu_item = MenuItem.objects.create(category=category, **validate_data)
        return menu_item



