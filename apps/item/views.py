# Django
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views import View
# Local
from settings.base import STRIPE_SECRET_KEY
from item.models import Item
# Python
from decouple import config
import stripe


stripe.api_key = STRIPE_SECRET_KEY


class ItemListView(View):
    def get(self, request):
        items = Item.objects.all()

        return render(request, "item_list.html", {
            "items": items,
            "stripe_public_key": config("STRIPE_PUBLIC_KEY"),
        })


class ItemDetailView(View):
    def get(self, request, id):
        item = get_object_or_404(Item, id=id)

        return render(request, "item.html", {
            "item": item,
            "stripe_public_key": config("STRIPE_PUBLIC_KEY"),
        })


class BuyItemView(View):
    def get(self, request, id):
        item = get_object_or_404(Item, id=id)

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": item.name,
                        "description": item.description,
                    },
                    "unit_amount": int(item.price * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="http://localhost:8800/",
            cancel_url="http://localhost:8800/",
        )

        return JsonResponse({"session_id": session.id})
