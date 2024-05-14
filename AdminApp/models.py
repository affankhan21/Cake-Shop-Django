from django.db import models

class Category(models.Model):
    cname=models.CharField(max_length=20)

    class Meta:
        db_table="Category"
    def __str__(self)->str:
        return self.cname    

class Cake(models.Model):
    cake_name=models.CharField(max_length=20)
    price=models.FloatField(default=400)
    description=models.CharField(max_length=100)
    image=models.ImageField(default="abc.jpg",upload_to="Images")   
    qty=models.IntegerField(default=10)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)     

    class Meta:
        db_table="Cake"