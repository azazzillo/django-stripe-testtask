# Django
from django.db import models
# Local
from item.models import Item


class Order(models.Model):

    STATUS_CREATED = "created"
    STATUS_PAID = "paid"
    STATUS_FAILED = "failed"

    STATUS_CHOICES = [
        (STATUS_CREATED, "Created"),
        (STATUS_PAID, "Paid"),
        (STATUS_FAILED, "Failed"),
    ]

    datetime_created = models.DateTimeField(
        verbose_name="дата создания",
    )
    total_amount = models.DecimalField(
        verbose_name="общая сумма",
        decimal_places=2,
        max_digits=11
    )
    stripe_payment_intent_id = models.CharField(
        verbose_name="stripe id",
        max_length=255,
        blank=True,
        null=True
    )
    status = models.CharField(
        verbose_name="статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED
    )

    class Meta: 
        db_table = "order"
        verbose_name = "заказ"
        verbose_name_plural = "заказы"
    
    def __str__(self):
        return f"{self.pk} | [{self.total_amount} $] |{self.datetime_created} | status: {self.status}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="заказ"
    )
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name="товар"
    )
    quantity = models.IntegerField(
        verbose_name="количество",
        default=1
    )
    price = models.DecimalField(
        verbose_name="цена",
        max_digits=11,
        decimal_places=2
    )

    class Meta:
        db_table = "order_item"
        verbose_name = "товар в заказе"
        verbose_name_plural = "товары в заказе"
    
    def __str__(self):
        return f"{self.item.name} ({self.quantity}) -> {self.order.pk}"
