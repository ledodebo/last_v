import uuid
from django.db import models
import datetime
from PIL import Image
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from django.conf import settings
from django_resized import ResizedImageField


class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) :
        return self.name

class size(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) :
        return self.name
    

class kind(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self) :
        return self.name


class checked(models.Model):
    checkedd =  models.CharField(max_length=50)
    def __str__(self) :
        return self.checkedd

class product(models.Model):
    name=models.CharField(max_length=50)
    image= ResizedImageField(size=[ 900, 1000],crop= ["middle", "center"],upload_to="uploads/product", force_format='PNG')
   
    descretion=models.CharField(max_length=250,default="",blank=True,null=True)
    
  
    def __str__(self) :
        return self.name
    
    def save(self, *args,**kwargs):
        super().save(*args,**kwargs)
        if self.image:
            size = (4578,5723)
            img  = Image.open(self.image.path)
            img.thumbnail(size,Image.LANCZOS)
            img.save(self.image.path)

class ProductVariation(models.Model):
    gender = (
        ('m',"male"),
        ('f',"female"),
        ('u',"unisex"),
    )
    brands = (
        ('v',"versatsse"),
        ('d',"dior"),
        ('M',"Mancera"),
    )
    brand = models.CharField(max_length=1,choices= brands)
    product = models.ForeignKey(product, related_name='variations', on_delete=models.CASCADE)
    size = models.ForeignKey(size,on_delete=models.CASCADE,default=0,null=True)
    type = models.ForeignKey(kind,on_delete=models.CASCADE,default=0,null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount=models.DecimalField(default=0,decimal_places=2,max_digits=6)
    ava=models.ForeignKey(checked,on_delete=models.CASCADE)
    genders = models.CharField(max_length=1,choices= gender)
    Category=models.ForeignKey(Category,on_delete=models.CASCADE,default=0,null=True)
    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.type}"
        
class gust(models.Model):
    name = models.CharField(max_length=100)
    device = models.CharField(max_length=100)
    def __str__(self) :
        return self.device

class CartItem(models.Model):
    ProductVariation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    device = models.CharField(max_length=100)
    gu = models.ForeignKey(gust, on_delete=models.CASCADE,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    session = models.CharField(max_length=100)
  
    def __str__(self):
        return f'{self.quantity} x {self.ProductVariation}'
    

class order(models.Model):
    zone = (
        ('c',"القاهرة"),
        ('g',"الجيزة"),
        ('a',"العصيد"),
        ('d',"الدلتا"),
        ('b',"الغردقة-البحر-الاحمر"),
        ('s',"شرم-الشيخ-جنوب سيناء"),
        ('n',"المدن-الجديدة"),
        ('m',"مدينة-بدر"),
        ('x',"اسكندرية"),
        ('xs',"اطراف-الاسكندرية"),
        ('q',"القناة"),
    )
    iteams = models.CharField(max_length=250) 
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    email =models.CharField(max_length=250) 
    name = models.CharField(max_length=250)
    zones = models.CharField(max_length=2,choices=zone)
    adress=models.CharField(max_length=250)
    phone=models.CharField(max_length=250)
    phone2=models.CharField(max_length=250)
    date=models.DateField(default=datetime.datetime.today)
    device = models.CharField(max_length=100)

    def __str__(self) :
        return self.adress
    
class inc(models.Model):
      user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
      phone=models.CharField(max_length=250)


class UserActivity(models.Model):
    ip_address = models.CharField(max_length=100, unique=True)  # Assuming IPv4 or IPv6
    phone_percentage = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.ip_address} - {self.timestamp}'