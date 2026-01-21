# Django
from django.urls import path
# Local
from item.views import ItemDetailView, BuyItemView, ItemListView


urlpatterns = [
    path('', ItemListView.as_view(), name="item_list"),
    path('item/<int:id>/', ItemDetailView.as_view(), name="item_detail"),
    path('buy/<int:id>/', BuyItemView.as_view(), name="buy_item"),
]
