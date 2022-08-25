from math import floor

from django.core.validators import MinValueValidator
from django.db.models import *
from django.utils import timezone


# Create your models here.
class Ingredient(Model):
    name = CharField(max_length=30, unique=True)
    stock = DecimalField(decimal_places=2, max_digits=6, default=0)
    price = DecimalField(validators=[MinValueValidator(0.009)], decimal_places=2, max_digits=6)

    def __str__(self):
        return self.name + " " + self.price.__str__() + " " + self.stock.__str__()

    def add(self, quantity):
        self.stock = self.stock + quantity

    def restock_needed(self):
        requirements = RecipeRequirement.objects.filter(ingredient=self)
        minimum = 0
        for requirement in requirements:
            minimum += requirement.menuItem.minStock * requirement.quantity
        return minimum - self.stock

    def total_restock(self):
        return round(self.restock_needed() * self.price, 2)


class MenuItem(Model):
    name = CharField(max_length=30)
    price = DecimalField(validators=[MinValueValidator(0.1)], decimal_places=2, max_digits=6)
    minStock = PositiveIntegerField(validators=[MinValueValidator(1)])
    deleted = BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name'], condition=Q(deleted=False), name='name of constraint')
        ]

    def __str__(self):
        return self.name + " " + self.price.__str__() + "$"

    def cost(self):
        recipes_requirement = RecipeRequirement.objects.filter(menuItem=self)
        total = 0
        for requirement in recipes_requirement:
            total += requirement.ingredient.price * requirement.quantity
        return round(total, 2)

    def stock(self):
        recipes_requirement = RecipeRequirement.objects.filter(menuItem=self)
        if not recipes_requirement.exists():
            return 0
        minimum = 9999999
        for requirement in recipes_requirement:
            avg = requirement.ingredient.stock / requirement.quantity
            if minimum > avg:
                minimum = avg
        return floor(minimum)

    def needs_stock(self):
        return self.minStock > self.stock()

    def purchase(self):
        Purchase.objects.create(menuItem=self)
        for recipe in RecipeRequirement.objects.filter(menuItem=self):
            ingredient = Ingredient.objects.filter(id=recipe.ingredient.id)
            new_stock = recipe.ingredient.stock - recipe.quantity
            ingredient.update(stock=new_stock)

    def delete_state(self):
        MenuItem.objects.filter(id=self.id).update(deleted=True)


class RecipeRequirement(Model):
    ingredient = ForeignKey(Ingredient, on_delete=CASCADE)
    menuItem = ForeignKey(MenuItem, on_delete=CASCADE)
    quantity = DecimalField(validators=[MinValueValidator(0.1)], decimal_places=1, max_digits=6, default=1)

    def __str__(self):
        return self.menuItem.name + ": " + self.quantity.__str__() + " " + self.ingredient.name

    def total(self):
        return round(self.quantity * self.ingredient.price, 2)


class Purchase(Model):
    menuItem = ForeignKey(MenuItem, on_delete=CASCADE)
    time = DateTimeField(default=timezone.now)

    def __str__(self):
        return self.menuItem.name + " " + self.time.__str__()
