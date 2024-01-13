from django.urls import path

from cart.views import add_products_to_cart_view, subtract_products_to_cart_view, remove_products_from_cart_view

urlpatterns = [
    # ajax
    path('add', add_products_to_cart_view),
    path('remove', remove_products_from_cart_view),
    path('subtract', subtract_products_to_cart_view),
]
