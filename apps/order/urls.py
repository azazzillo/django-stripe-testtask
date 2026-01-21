# Django
from django.urls import path
# Local
from order.views import OrderCreateView, OrderPayView


urlpatterns = [
    path('pay/<int:id>/', OrderPayView.as_view(), name="order_pay"),
    path('create/', OrderCreateView.as_view(), name="order_create"),
]
