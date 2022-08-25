from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.Home.as_view(), name='home'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('restock/', views.restock, name='restock'),
    path('menu/', views.menu, name='menus'),
    path('menu/<pk>/', views.menu_detail, name='menu'),
    path('menu/<pk>/ingredients/', views.add_recipe_ingredient, name='recipe_ingredients'),
    path('purchases/', views.ViewPurchases.as_view(), name='purchases'),
]
