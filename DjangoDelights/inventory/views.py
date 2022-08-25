from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.management import call_command
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView
from django_filters.views import FilterView
from .filters import IngredientFilter, MenuItemFilter, PurchaseFilter
from .forms import IngredientForm, MenuItemForm
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .functions import filter_name, pagination


# Create your views here.


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'


def login_view(request):
    call_command('migrate', verbosity=0)
    call_command('loaddata', 'initial_db.json', verbosity=0)
    logout(request)
    error = ''
    if 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            call_command('flush', verbosity=0, interactive=False)
            call_command('loaddata', 'initial_db.json', verbosity=0)
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            error = 'Incorrect'
    return render(request, "registration/login.html", {'error': error})


@login_required
def ingredients(request):
    context = {"object_list": Ingredient.objects.all().order_by('name'), "form": IngredientForm()}

    # Ingredient Update
    if request.method == 'POST':
        if 'id' in request.POST and Ingredient.objects.filter(id=request.POST['id']):
            ingredient = Ingredient.objects.get(id=request.POST['id'])

            # Add Stock
            if 'stock' in request.POST:
                ingredient.add(int(request.POST['stock']))
                ingredient.save()

            # Delete
            elif 'delete' in request.POST:
                ingredient.delete()
        else:

            # Form
            context['form'] = IngredientForm(request.POST)
            if context['form'].is_valid():
                context['form'].save()

            print(context['form'])

    # Queryset
    if context['object_list']:
        context['object_list'] = filter_name(request, context['object_list'])
    total = 0
    for ingredient in context['object_list']:
        total += ingredient.price * ingredient.stock
    context['total'] = round(total, 2)

    # Pagination
    context = pagination(request, context)

    # Filter
    context['filter'] = IngredientFilter(request.GET, queryset=context['object_list'])

    return render(request, "inventory/ingredient.html", context)


@login_required
def menu(request):
    context = {"object_list": MenuItem.objects.filter(deleted=False).order_by('name'), "form": MenuItemForm()}

    # Menu Update
    if request.method == 'POST':
        if 'id' in request.POST and MenuItem.objects.filter(id=request.POST['id']):
            obj = MenuItem.objects.get(id=request.POST['id'])

            # Delete
            if 'delete' in request.POST:
                obj.delete_state()

            # Purchase
            if 'purchase' in request.POST and obj.stock() != 0:
                obj.purchase()

        else:
            # Form
            context['form'] = MenuItemForm(request.POST)
            if context['form'].is_valid():
                obj = context['form'].save()
                return HttpResponseRedirect(reverse('menu', kwargs={'pk': obj.pk}))

    # Queryset
    if context['object_list']:
        context['object_list'] = filter_name(request, context['object_list'])

    # Pagination
    context = pagination(request, context)

    # Filter
    context['filter'] = MenuItemFilter(request.GET, queryset=context['object_list'])

    return render(request, "inventory/menu.html", context)


@login_required
def menu_detail(request, pk):
    context = {"menu": MenuItem.objects.get(pk=pk),
               "object_list": RecipeRequirement.objects.filter(menuItem=MenuItem.objects.get(pk=pk))
               .order_by('menuItem__name')}

    # Recipe Update
    if request.method == 'POST':
        if 'id' in request.POST and RecipeRequirement.objects.filter(id=request.POST['id']):
            recipe = RecipeRequirement.objects.filter(id=request.POST['id'])

            # Update Recipe
            if 'quantity' in request.POST and recipe:
                recipe.update(quantity=request.POST['quantity'])

            # Delete
            elif 'delete' in request.POST:
                recipe.delete()

    # Queryset
    if context['object_list']:
        context['object_list'] = filter_name(request, context['object_list'])

    # Pagination
    context = pagination(request, context)

    # Filter
    context['filter'] = IngredientFilter(request.GET, queryset=context['object_list'])

    return render(request, "inventory/menu_detail.html", context)


@login_required
def add_recipe_ingredient(request, pk):
    context = {"object_list": Ingredient.objects.all().order_by('name'), "menu": MenuItem.objects.get(pk=pk)}

    # Recipe Update
    if request.method == 'POST':
        if 'id' in request.POST and Ingredient.objects.filter(id=request.POST['id']):
            ingredient = Ingredient.objects.get(id=request.POST['id'])
            recipe = RecipeRequirement.objects.create(ingredient=ingredient, menuItem=context['menu'])
            recipe.save()

    # Queryset
    if context['object_list']:
        context['object_list'] = filter_name(request, context['object_list'])

    recipes = RecipeRequirement.objects.filter(menuItem=context['menu'])
    for recipe in recipes:
        context['object_list'] = context['object_list'].exclude(id=recipe.ingredient.id)

    context = pagination(request, context)

    # Filter
    context['filter'] = IngredientFilter(request.GET, queryset=context['object_list'])

    return render(request, "inventory/recipe_ingredient.html", context)


class ViewPurchases(LoginRequiredMixin, FilterView):
    model = Purchase
    filterset_class = PurchaseFilter
    paginate_by = 10
    ordering = ['time']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchases = Purchase.objects.all()
        if 'menuItem__name' in self.request.GET:
            purchases = purchases.filter(menuItem__name__contains=self.request.GET['menuItem__name'])
        revenue = 0
        cost = 0
        for purchase in purchases:
            revenue += purchase.menuItem.price
            cost += purchase.menuItem.cost()
        context['revenue'] = revenue
        context['profit'] = round(revenue - cost, 2)
        return context


@login_required
def restock(request):
    context = {"object_list": Ingredient.objects.all()}
    for ingredient in context['object_list']:
        if ingredient.restock_needed() <= 0:
            context['object_list'] = context['object_list'].exclude(id=ingredient.id)

    # Recipe Update
    if request.method == 'POST' and 'restock' in request.POST:
        for ingredient in context['object_list']:
            ingredient.add(ingredient.restock_needed())
            ingredient.save()
        return HttpResponseRedirect(reverse('ingredients'))

    # Queryset
    if context['object_list']:
        context['object_list'] = filter_name(request, context['object_list'])
    total = 0
    for ingredient in context['object_list']:
        total += ingredient.total_restock()
    context['total'] = round(total, 2)

    context = pagination(request, context)

    # Filter
    context['filter'] = IngredientFilter(request.GET, queryset=context['object_list'])

    return render(request, "inventory/restock.html", context)
