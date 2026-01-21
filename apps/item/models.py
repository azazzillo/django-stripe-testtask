# Django
from django.db import models


class Item(models.Model):
    name = models.CharField(
        max_length=220,
        verbose_name="название"
    )
    description = models.TextField(
        verbose_name="описание"
    )
    price = models.DecimalField(
        verbose_name="цена",
        max_digits=11,
        decimal_places=2
    )

    class Meta:
        db_table = "item"
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return f"{self.name} | {self.price}"
