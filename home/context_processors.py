
from .models import CartItem,ProductVariation
from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, HttpResponse
from django.http import HttpResponseRedirect
def items_count(requset):
   if requset.user.is_authenticated:
      a = CartItem.objects.filter(user=requset.user).count()
      message = ("FREE DELIVERY TO YOUR HOME FROM EGP 1000")
      cart_items = CartItem.objects.filter(user=requset.user)
      total_price = sum(item.ProductVariation.discount * item.quantity for item in cart_items)
      offer = round(1000-total_price)
      if total_price > 1:
         offer = round(1000-total_price)
         message = ((str(offer))+"LEFT FOR THE FREE DELIVERY OFFER")
      if total_price >= 1000 :
         message = ("NOW YOU HAVE FREE DELIVERY")
      else :
            message = ("FREE DELIVERY TO YOUR HOME FROM EGP 1000")
      
      return {'items_count':a,'offer':message}
   else:
       device = requset.COOKIES.get('device')
       a = CartItem.objects.filter(device=device).count()
       message = ("FREE DELIVERY TO YOUR HOME FROM EGP 1000")
       cart_items = CartItem.objects.filter(device=device)
       total_price = sum(item.ProductVariation.discount * item.quantity for item in cart_items)
       offer = round(1000-total_price)
       if total_price > 1:
         offer = round(1000-total_price)
         message = ((str(offer))+"LEFT FOR THE FREE DELIVERY OFFER")
       if total_price >= 1000 :
         message = ("NOW YOU HAVE FREE DELIVERY")
       else :
            message = ("FREE DELIVERY TO YOUR HOME FROM EGP 1000")
       return {'items_count':a,'offer':message}
    

