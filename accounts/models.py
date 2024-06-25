from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from home.models import product
import datetime





class customer(models.Model):
    usser = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    phone=models.CharField(max_length=50)
    device = models.CharField(max_length=100)
    catagofavry=models.ForeignKey(product,on_delete=models.CASCADE,null=True)
    #order = customer=models.ForeignKey(order,on_delete=models.CASCADE,null=True)
    def __str__(self) :
        return str(self.usser)
    



   
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        customer.objects.create(usser=instance)


  

