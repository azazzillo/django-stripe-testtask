# Django
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.utils import timezone
from django.views import View
# Local
from order.models import Order, OrderItem
from item.models import Item
# Python
from decouple import config
import stripe 
import json


@method_decorator(csrf_exempt, name="dispatch")
class OrderCreateView(View):
    def post(self, request):
        data = json.loads(request.body)

        order = Order.objects.create(
            datetime_created=timezone.now(),
            total_amount=0
        )

        total = 0

        for i in data["items"]:
            item = Item.objects.get(id=i["item_id"])
            quantity = i.get("quantity", 1)

            OrderItem.objects.create(
                order=order,
                item=item,
                quantity=quantity,
                price=item.price
            )

            total += item.price * quantity
        
        order.total_amount = total
        order.save()

        return JsonResponse({
            "order_id": order.id,
            "total_amount": float(total),
            "stripe_public_key": config("STRIPE_PUBLIC_KEY"),
        })


class OrderPayView(View):
    def get(self, request, id):
        order = get_object_or_404(Order, id=id)

        order_items = order.items.all()

        line_items = []
        for oi in order_items:
            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": oi.item.name,
                        "description": oi.item.description
                    },
                    "unit_amount": int(oi.price * 100),
                },
                "quantity": oi.quantity,
            })

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url="http://localhost:8000/",
            cancel_url="http://localhost:8000/"
        )

        return JsonResponse({
            "session_id": session.id,
            "stripe_public_key": config("STRIPE_PUBLIC_KEY"),
        })
