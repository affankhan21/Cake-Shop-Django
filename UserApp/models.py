from django.db import models
from AdminApp.models import Cake
from datetime import datetime

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    password  = models.CharField(max_length=20)
    email = models.EmailField(max_length = 100)
    class Meta:
        db_table = "UserInfo"

    def __str__(self):
        return self.username
    
class Payment(models.Model):
    card_no = models.CharField(max_length=10,primary_key=True)
    cvv = models.CharField(max_length=10)
    expiry = models.CharField(max_length=10)
    balance = models.FloatField(default=10000)
    class Meta:
        db_table = "Payment"
    
class Order_Master(models.Model):
    date_of_order = models.DateField(default = datetime.now())
    amount = models.FloatField(default=1000)
    user = models.ForeignKey(UserInfo,on_delete=models.SET_NULL,null=True)
    class Meta:
        db_table = "OrderMaster"

class Status(models.Model):
    status_name = models.CharField(max_length=20)
    class Meta:
        db_table = "Status"
    
class MyCart(models.Model):
    cake = models.ForeignKey(Cake,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(UserInfo,on_delete=models.SET_NULL,null=True)
    qty = models.IntegerField(default=1)
    status  = models.ForeignKey(Status,on_delete=models.CASCADE,default=2)
    order_id = models.ForeignKey(Order_Master,on_delete = models.CASCADE,null=True)
    class Meta:
        db_table = "MyCart"