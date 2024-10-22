from django.contrib.auth.models import User
from django.db import models

from product_admin.models import Add_Productmaster


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneNo = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)


class Add_to_cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    addProduct=models.ForeignKey(Add_Productmaster,on_delete=models.CASCADE)
    product_quantity=models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.addProduct:
            self.total_price = self.addProduct.product_price * self.product_quantity
        super(Add_to_cart, self).save(*args, **kwargs)


class Wishlist(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Add_Productmaster,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name}"


class Place_to_order(models.Model):
    PAYMENT_CHOICES = [
        ('razorpay', 'Razorpay'),
        ('cash_on_delivery', 'Cash on Delivery'),
    ]

    STATUS_CHOICES = [
        ('pending','Pending'),
        ('delivered','Delivered'),
        ('cancelled','Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pincode = models.IntegerField()
    payment_option = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash_on_delivery')
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')

    def __str__(self):
        return f"Order by {self.user} - {self.payment_option}"


class Confirm_order(models.Model):
    user =models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Add_Productmaster,on_delete=models.CASCADE)
    placeorder=models.ForeignKey(Place_to_order,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    final_total_price=models.FloatField(default=0)
    quantity=models.IntegerField(default=False)




