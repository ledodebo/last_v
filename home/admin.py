from django.contrib import admin
from .models import Category,product,CartItem,inc,gust,order,ProductVariation,checked,size,kind,UserActivity




admin.site.register(Category)
admin.site.register(UserActivity)
admin.site.register(CartItem)
admin.site.register(product)
admin.site.register(order)
admin.site.register(kind)
admin.site.register(size)
admin.site.register(gust)
admin.site.register(checked)
admin.site.register(inc)
admin.site.register(ProductVariation)
