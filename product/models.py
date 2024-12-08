from django.db import models
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("Name"))
    code = models.CharField(max_length=250, verbose_name=_("Code"), unique=True)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=250, verbose_name=_("Name"))

    def __str__(self):
        return self.name


class ProductMaterial(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True, default=0,
                                   verbose_name=_("Quantity"))

    def __str__(self):
        return f"{self.product.name} for {self.material.name}"


class Warehouse(models.Model):
    material = models.ForeignKey('Material', on_delete=models.CASCADE)
    remainder = models.IntegerField(null=True, blank=True, verbose_name=_("Remainder"))
    price = models.FloatField(null=True, blank=True, verbose_name=_("Price"), default=0)

    def __str__(self):
        return f"{self.material.name} ({self.remainder})"
