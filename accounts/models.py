from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):  #ParentModel
    user = models.OneToOneField (User, null = True, on_delete=models.CASCADE ,related_name="customer",blank=True)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200,null=True)
    email = models.CharField(max_length=200,null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    profile_pic = models.ImageField(null=True, blank=True, default="c.jpg")

    def __str__(self):
        return self.name
    
class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.name   
    
class Product(models.Model): #ParentModel
    CATEGORY = (
        ('Indoor','Indoor'),
        ('OutDoor',"Outdoor")
    )
    name = models.CharField(max_length=200, null = True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name  

class Order(models.Model): #ChildModel
    STATUS = (
        ('Pending','Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered')
    )
    
    customer = models.ForeignKey(Customer, null=True, on_delete= models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete= models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True, null=True)  
    status = models.CharField(max_length=200, null=True, choices= STATUS)
    note = models.CharField(max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return str(self.product)


# querset = ModelName.objects(model objects attribute).method(all,get, filter, exclude)

