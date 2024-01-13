from django.urls import path
from .views import HomePageView, CategoryPageView, ProductPage, get_linked_product_info_view, get_filtered_products_view

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('category/<slug>', CategoryPageView.as_view(), name='category'),
    path('product/<slug>', ProductPage.as_view(), name='product'),


    # ajax
    path('linked_prod_info', get_linked_product_info_view),
    path('get_filtered_products', get_filtered_products_view),
]