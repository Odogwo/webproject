from django.db import models

# Create your models here.

class Product(models.Model):
	product_name = models.CharField(max_length=150, null=True)
	product_type = models.CharField(max_length=25,null=True)
	product_description = models.TextField(default="No Description")
	affiliate_url = models.SlugField(blank=True, null=True)
	product_image = models.ImageField(upload_to='images/', null=True)

	def __str__(self):
		return self.product_name