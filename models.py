from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

class Add_Productmaster(models.Model):
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_img = models.ImageField(upload_to='product_images/')
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)



