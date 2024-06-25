from .models import product,ProductVariation
import django_filters


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = (ProductVariation)
        fields = '__all__'
        exclude = ["ava","name","discount","price","product","type"]


"""    
class orderFilter(django_filters.FilterSet):
    class Meta:
        model = order
        fields = '__all__'
        exclude = ["user","status","date","quantity"]
"""  
