from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# related_name is a Django model field option that creates a reverse relationship from the referenced model
# back to the model containing the ForeignKey.

# - Access the restaurant from a user: `user.managed_restaurant`
# - Access all users (managers) who manage a restaurant: `restaurant.managers.all()`
# - Access the chain from a restaurant: `restaurant.chain`
# - Access all restaurants in a chain: `chain.restaurants.all()`

class User(AbstractUser):
    is_kitchen = models.BooleanField(default=False)
    # Add this field to store which restaurant a merchant manages
    managed_restaurant = models.ForeignKey(
        'Restaurant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managers'
    )
    def __str__(self):
        return self.username + " - kitchen: " + str(self.is_kitchen)

class Chain(models.Model):
    chain_name = models.CharField(max_length=100)

    def __str__(self):
        return self.chain_name


# The related_name in Django allows you to access the reverse relationship from the 
# related model back to the model where the relationship is defined.
# in this case, Chain and Cuisines are the related models and Restaurant is the model where the relationship is defined.

# Access all restaurants of a specific chain
# chain_instance = Chain.objects.get(id=1)
# chain_restaurants = chain_instance.locations.all()

class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    # Add the new address field
    address = models.CharField(max_length=255, blank=True, null=True)
    chain = models.ForeignKey(Chain, on_delete=models.SET_NULL, null=True, blank=True, related_name='branches')
    cuisine = models.CharField(max_length=100, blank=True, null=True)
    rating = models.DecimalField(
        max_digits=2, 
        decimal_places=1,
        validators=[
            MinValueValidator(1.0),
            MaxValueValidator(5.0)
        ]
    )
    opening_time = models.TimeField(default=timezone.now().replace(hour=9, minute=0, second=0, microsecond=0).time())
    closing_time = models.TimeField(default=timezone.now().replace(hour=22, minute=0, second=0, microsecond=0).time())
    # upload_to parameter specifies the directory where the images will be stored relative to your media root.
    image = models.ImageField(upload_to='restaurant_images/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    # Add this method to get all orders for this restaurant
    def get_orders(self):
        return Order.objects.filter(restaurant=self)

class MenuCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, default=None)
    category_name = models.CharField(max_length=200)
    def __str__(self):
        return self.restaurant.name + " - " + self.category_name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True, null=True)  # Add this line
    category = models.ForeignKey(MenuCategory, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='menu_items/')
    is_available = models.BooleanField(default=True, null=True)  # Add null=True temporarily

    def __str__(self):
        return self.restaurant.name + " - " + self.item_name

class Order(models.Model):
    STATUS_CHOICES = [
        ('incart', 'In Cart'),
        ('checkout', 'Checked Out'),
        ('paid', 'Paid'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_orders')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    # items: This field represents the many-to-many relationship between Order and MenuItem.
    # through parameter specifies the intermediate model (OrderItem) that will be used to manage this many-to-many relationship 
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='incart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.restaurant.name + " - " + self.customer.username + " - " + self.status

# through='OrderItem': This specifies that the OrderItem model is used to manage the relationship,
# allowing for additional fields like quantity and special_instructions to be associated with each item in an order.
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    special_instructions = models.TextField(blank=True)
    
    @property
    def total_price(self):
        return self.menu_item.price * self.quantity
    

class Cancellation(models.Model):
    CANCELLATION_REASONS = [
        ('unavailable', 'Items unavailable'),
        ('customer', 'Customer canceled'),
        ('closed', 'Store closed'),
        ('busy', 'Store Busy'),
        ('others', 'Others'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=CANCELLATION_REASONS, default='others')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
