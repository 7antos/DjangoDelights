# DjangoDelights
Application that will help track of how much food they have throughout the day. The owner starts the day with:

- An inventory of different Ingredients, their available quantity, and their prices per unit.
- A list of the restaurant’s MenuItems, and the price set for each entry.
- A list of the ingredients that each menu item requires (RecipeRequirements).
- A log of all Purchases made at the restaurant. 

Knowing that information, the restaurant, Django Delights’ owner has asked for the following features:

1. They should be able to enter in new recipes along with their recipe requirements, and how much that menu item costs.
2. They should also be able to add to the inventory a name of an ingredient, its price per unit, and how much of that 
item is available.
3. They should be able to enter a customer purchase of a menu item. When a customer purchases an item off the menu, 
the inventory should be modified to accommodate what happened, as well as recording the time that the purchase was made.

## Database

### Ingredient
Attributes: varchar Name, int Quantity, double Price
Method: void Add(int quantity)

### RecipeRequirement
Attribute: pk ingredient, pk recipe, int quantity

### MenuItem
Attributes: varchar Name, double Price, int minStock

### Purchase
Attributes: pk MenuItem, time

## Endpoints

- [x] Information about the total cost of inventory
- [x] Total revenue for the day
- [x] Different purchases that were made
- [x] How much inventory is required to restock

## Requirements

- [x] Users can log in, log out, and must be logged in to see the views
- [x] Users can create items for the menu
- [x] Users can add ingredients to the restaurant’s inventory and update their quantities
- [x] Users can add the different recipe requirements for each menu item
- [x] Users can record purchases of menu items (only the ones that are able to created with what’s in the inventory!)
- [x] Users can view the current inventory, menu items, their ingredients, and a log of all purchases made

## Installation

### Windows

1. Download e install [Python](https://www.python.org/downloads/)
2. Project Clone: ```git clone https://github.com/7antos/DjangoDelights.git```
3. Enter Project Directory: ```cd DjangoDelights```
4. Run Bat File: ```install.bat```
5. Run Server: ```python manage.py runserver```

### Linux

1. Download e install [Python](https://www.python.org/downloads/)
2. Project Clone: ```git clone https://github.com/7antos/DjangoDelights.git```
3. Enter Project Directory: ```cd DjangoDelights```
4. Run Bash File: ```sudo ./install.sh```
5. Run Server: ```python manage.py runserver```
