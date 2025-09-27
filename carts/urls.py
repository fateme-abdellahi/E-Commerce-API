from django.urls import path

from .views import CartApiView

urlpatterns = [
    path('carts/', CartApiView.as_view(), name='carts'),
]
