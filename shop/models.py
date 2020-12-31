from django.db import models
from django.contrib.auth.models import User


# Create your models here

# class UserProfileInfo(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)

# def __str__(self):
#     return self.user.username
    




    


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50,default="")
    subcategory = models.CharField(max_length=50,default="")
    price = models.IntegerField(default=0)
    
    product_desc = models.CharField(max_length=300)
    product_date = models.DateField()
    image = models.ImageField(upload_to="shop/images",default="")


    def __str__(self):
        return self.product_name



class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    phone = models.CharField(max_length=70, default="")
    desc = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=111)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=70, default="")


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default = "")
    # order_id = models.ForeignKey(Orders,to_field=id',on_delete=models.CASCADE)
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."



class SlidesImgaes(models.Model):
    slide_id = models.AutoField
    slide_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
        return self.slide_name





# Creating module for customer registration
# class Customer(models.Model):
#     customer_id = models.AutoField(primary_key=True)
#     customer_name = models.CharField(max_length=70)
    
#     customer_email = models.EmailField(max_length=70, default="")
#     # customer_phone = models.CharField(max_length=13, default="")
#     customer_phone  =models.IntegerField( unique=True)
#     password = models.CharField(max_length=500)

#     def __str__(self):
#         return self.customer_name