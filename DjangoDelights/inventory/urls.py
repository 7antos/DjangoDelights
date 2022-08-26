from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('assets/favicon.ico'))),
    path('login/', views.login_view, name='login'),
    path('', views.Home.as_view(), name='home'),
    path('ingredients/', views.ingredients, name='ingredients'),
    path('restock/', views.restock, name='restock'),
    path('menu/', views.menu, name='menus'),
    path('menu/<pk>/', views.menu_detail, name='menu'),
    path('menu/<pk>/ingredients/', views.add_recipe_ingredient, name='recipe_ingredients'),
    path('purchases/', views.ViewPurchases.as_view(), name='purchases'),
]
