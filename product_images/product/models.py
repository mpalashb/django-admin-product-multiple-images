from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True, default=0.0)
    thumbnail = models.ImageField(
        blank=True, null=True, upload_to='product_images/thumbnail/')

    def __str__(self) -> str:
        return f"{self.title} - {self.pk}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, related_name='all_images')
    image = models.ImageField(upload_to='product_images/images/')
