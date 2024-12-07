from django.urls import path
from Web.views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('products/', get_products, name='products'),
    path('products/create/', create_product, name='create_product'),
    path('products/<int:pk>/update/', update_product, name='update_product'),
    path('products/<int:pk>/delete/', delete_product, name='delete_product'),
    path('categories/', get_categories, name='categories'),
    path('categories/create/', create_category, name='create_category'),
    path('categories/<int:pk>/update/', update_category, name='update_category'),
    path('categories/<int:pk>/delete/', delete_category, name='delete_category'),
]
