# Django
from django.urls import path, include
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('item.urls')),
    path('order/', include('order.urls'))
]
