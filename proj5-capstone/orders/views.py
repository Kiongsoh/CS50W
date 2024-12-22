from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, HttpResponseRedirect, render, redirect
from django.urls import reverse
from django.db import IntegrityError
from .models import Restaurant, MenuItem, Order, OrderItem, User

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
import traceback
import json

from django.contrib import messages
from django.core.files.storage import default_storage
from django.views.decorators.http import require_http_methods


# i think currently the status are not tagged correctly.
# for example, when customer order, the status is 'accepted' but not 'pending'

def restaurant_selection(request):
    # Fetch all restaurants from the database
    restaurants = Restaurant.objects.all()
    # Render the restaurant selection page with the list of restaurants
    return render(request, 'orders/restaurant_selection.html', {'restaurants': restaurants})

def menu_display(request, restaurant_id):
    # Get the specific restaurant based on the restaurant_id
    restaurant = Restaurant.objects.get(id=restaurant_id)
    # Fetch all menu items for this restaurant
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    # Render the menu selection page with restaurant and menu items
    return render(request, 'orders/menu_display.html', {'restaurant': restaurant, 'menu_items': menu_items})

# Add this new function to handle AJAX authentication errors
def handle_ajax_login_required(request):
    return JsonResponse({
        'success': False,
        'error': 'authentication_required',
        'message': 'Please log in to continue',
        'login_url': reverse('login')  # Add this to provide the login URL
    }, status=401)


@login_required #This decorator ensures that only authenticated users can access the view
@require_POST #This decorator restricts the view to only accept POST requests - POST is used for creating or updating resources
@csrf_protect #This decorator is used to protect the view against Cross-Site Request Forgery (CSRF) attacks - it is used to verify that the request originates from your site and not from a third party
def add_to_order(request):
    # 1. Parse the JSON data from the request body
    # 2. Check if item_id is provided
    # 3. Get the MenuItem object
    # 4. Get or create an Order for the current user with 'incart' status
    # 5. Get or create an OrderItem for this menu item in the order
    # 6. If the OrderItem already existed, increment its quantity
    # 7. Update the total price of the order
    # 8. Return a success response  

    # Parse the JSON data from the request body
    data = json.loads(request.body)
    item_id = data.get('item_id')
    force_new = data.get('force_new', False)  # New parameter to handle user confirmation

    # Check if item_id is provided
    if not item_id:
        return JsonResponse({'success': False, 'error': 'Item ID is required'}, status=400)
    
    try:
        # Get the MenuItem object
        menu_item = MenuItem.objects.get(id=item_id)                

        # Check if there's an existing cart with items from a different restaurant
        existing_order = Order.objects.filter(
            customer=request.user,
            status='incart'
        ).first()

        if existing_order and existing_order.restaurant != menu_item.restaurant:
            if not force_new:
                # If force_new is False, return a special response indicating different restaurant
                return JsonResponse({
                    'success': False,
                    'error': 'different_restaurant',
                    'message': f'You have items in your cart from {existing_order.restaurant.name}. Adding this item will clear your current cart. Would you like to continue?'
                })
            else:
                # If force_new is True, delete the existing order
                existing_order.delete()

        # get_or_create is used to get an existing order or create a new one if it doesn't exist
        # Get or create an Order for the current user with 'incart' status
        # it will return a Tuple of order object and a boolean value
        # <Order: Order object (1)>
        # True if a new object was created, or False if an existing object was retrieved.
        
        # Create new order or get existing one from same restaurant
        order, created = Order.objects.get_or_create(
            customer=request.user,
            status='incart',
            defaults={'restaurant': menu_item.restaurant, 'total_price': 0}
        )

        # Get or create OrderItem for this menu item in the order
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            menu_item=menu_item,
            defaults={'quantity': 1}
        )

        # If the OrderItem already existed, increment its quantity
        if not created:
            order_item.quantity += 1
            order_item.save()

        # Update the total price of the order
        order.total_price += menu_item.price
        order.save()

        # Return a success response
        return JsonResponse({'success': True})

    except MenuItem.DoesNotExist:
        # Handle the case where the menu item doesn't exist
        return JsonResponse({'success': False, 'error': 'Menu item not found'}, status=404)
    except Exception as e:
        # Handle any other exceptions that might occur
        # more detailed error logging
        print(f"Error in add_to_order: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# ---------------------------------------------------------------------------------------

@login_required #This decorator ensures that only authenticated users can access the view
@require_POST #This decorator restricts the view to only accept POST requests - POST is used for creating or updating resources
@csrf_protect #This decorator is used to protect the view against Cross-Site Request Forgery (CSRF) attacks - it is used to verify that the request originates from your site and not from a third party
def remove_from_order(request):
    # Parse the JSON data from the request body
    data = json.loads(request.body)
    item_id = data.get('item_id')

    # Check if item_id is provided
    if not item_id:
        return JsonResponse({'success': False, 'error': 'Item ID is required'}, status=400)
    
    try:
        # Get the MenuItem object
        menu_item = MenuItem.objects.get(id=item_id)                

        # Get an Order for the current user with 'incart' status
        order = Order.objects.get(customer=request.user, status='incart')

        # Get or create an OrderItem for this menu item in the order
        order_item = OrderItem.objects.get(order=order, menu_item=menu_item)
        
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
        else:
            order_item.delete()
        
        # Update the total price of the order
        order.total_price -= menu_item.price
        order.save()

        # Return a success response
        return JsonResponse({'success': True})

    except (MenuItem.DoesNotExist, Order.DoesNotExist, OrderItem.DoesNotExist):
        # Handle the case where the menu item doesn't exist
        return JsonResponse({'success': False, 'error': 'Item not found in order'}, status=404)
    
    except Exception as e:
        # Handle any other exceptions that might occur
        # more detailed error logging
        print(f"Error in add_to_order: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

# ---------------------------------------------------------------------------------------
@login_required
@csrf_protect
# this function is used to get the total cart quantity in the navbar
def get_cart_quantity(request):
    print("get_cart_quantity view called")  # Add this line
    try:
        order = Order.objects.get(customer=request.user, status='incart')
        # orderitem_set: This is automatically created by Django for reverse relations.
        # It's named after the model (OrderItem) in lowercase, followed by _set.
        # .all(): This method retrieves all related OrderItem objects for the given Order.
        # sum(): This function calculates the total sum of the quantity field for all OrderItem objects in the queryset.
        quantity = sum(item.quantity for item in order.orderitem_set.all())
        print(quantity)
    except Order.DoesNotExist:
        quantity = 0
    return JsonResponse({
        'quantity': quantity,
        'total_price': order.total_price
        })
# ---------------------------------------------------------------------------------------
@login_required
@csrf_protect #This decorator is used to protect the view against Cross-Site Request Forgery (CSRF) attacks - it is used to verify that the request originates from your site and not from a third party
def get_item_quantities(request):
    try:
        # Get the current user's cart
        order = Order.objects.get(customer=request.user, status='incart')
        
        # Create a dictionary of item_id: quantity pairs
        # .all(): This method retrieves all related OrderItem objects for the given Order.
        quantities = {
            item.menu_item.id: item.quantity 
            for item in order.orderitem_set.all()
        }

        total_prices = {
            item.menu_item.id: item.total_price 
            for item in order.orderitem_set.all()
        }
        
        # print(f"Retrieved quantities: {quantities}")  # Debug print
        print(f"Retrieved prices: {total_prices}")  # Debug print
        return JsonResponse({
            'success': True,
            'quantities': quantities,
            'total_prices': total_prices})
        
    except Order.DoesNotExist:
        # If no order exists, return empty quantities
        return JsonResponse({'success': True, 'quantities': {}})
    except Exception as e:
        print(f"Error in get_item_quantities: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
def view_cart(request):
    try:
        # Try to get the pending order for the current user
        order = Order.objects.get(customer=request.user, status='incart')
    except Order.DoesNotExist:
        # If no pending order exists, set order to None
        order = None
    # Render the cart page with the current order (if it exists)
    return render(request, 'orders/cart.html', {'order': order})

@login_required
def checkout(request):
    # if request.method == 'POST':
        # Change the order status to 'accepted'
        # order.status = 'accepted'
        # order.save()
        # Redirect to the order confirmation page
        # return redirect('order_confirmation')
    try:
        # Try to get the pending order for the current user
        order = Order.objects.get(customer=request.user, status='incart')
    except Order.DoesNotExist:
        # If no pending order exists, set order to None
        order = None    
    # If it's a GET request, just render the checkout page
    return render(request, 'orders/checkout.html', {'order': order})

# incart > checkout > accepted > completed > cancelled
# customer order submission button
@login_required
def order_confirmed(request):
    if request.method == 'POST':
        order = Order.objects.get(customer=request.user, status='incart')
        # Change the order status to 'checkout'
        order.status = 'paid'
        order.save()
        # Redirect to the order confirmation page
        return render(request, 'orders/order_confirmed.html', {'order': order})
    return render(request, 'orders/checkout.html', {'order': order})


@login_required
def history(request):
    try:
        # Get all orders
        orders = Order.objects.filter(customer=request.user).exclude(status='incart').order_by('-created_at')
    except len(orders) == 0:
        # If no pending order exists, set order to None
        orders = None    
    # If it's a GET request, just render the checkout page
    return render(request, 'orders/history.html', {'orders': orders})

# kitchen user functions
# ---------------------------------------------------------------------------------------
@login_required
def kitchen_orders(request):
    # Check if the user is kitchen staff
    if not request.user.is_kitchen:
        return redirect('restaurant_selection')
    
    # Check if the user has a managed restaurant
    if not request.user.managed_restaurant:
        return render(request, "kitchen/kitchen_orders.html", {
            "message": "No restaurant assigned to your account. Please contact admin.",
            "orders": []
        })
    
    # Get all orders for this restaurant except those with 'incart' status
    orders = Order.objects.filter(
        restaurant=request.user.managed_restaurant,
        status__in=['paid', 'accepted']
    ).order_by('-created_at')  # Most recent orders first
    
    return render(request, 'kitchen/kitchen_orders.html', {'orders': orders})

@login_required
def kitchen_history(request):
    # Check if the user is kitchen staff
    if not request.user.is_kitchen:
        return redirect('restaurant_selection')
    
    # Check if the user has a managed restaurant
    if not request.user.managed_restaurant:
        return render(request, "kitchen/kitchen_orders.html", {
            "message": "No restaurant assigned to your account. Please contact admin.",
            "orders": []
        })
    
    # Get all orders for this restaurant except those with 'incart' status
    orders = Order.objects.filter(
        restaurant=request.user.managed_restaurant,
    ).exclude(
        status='incart'
    ).order_by('-created_at')  # Most recent orders first
    
    return render(request, 'kitchen/kitchen_history.html', {'orders': orders})


# kitchen accept order button
@login_required
@require_POST  # Add this decorator to ensure only POST requests are accepted
def update_status(request, order_id):
    # Check if the user is kitchen staff
    if not request.user.is_kitchen:
        # If not, redirect them to the restaurant selection page
        return redirect('restaurant_selection')
    
    try:
        # Get the specific order based on the order_id
        order = Order.objects.get(id=order_id)
        # Get the action type from the POST data ('accept' or 'cancel')
        action = request.POST.get('action')
        # Get the next URL from POST data, default to kitchen_orders
        next_page = request.POST.get('next', 'kitchen_orders')

        # Update order status based on the action
        if action == 'accept':
            # Change the order status to 'accepted'
            order.status = 'accepted'
        elif action == 'cancel':
            # Change the order status to 'cancelled'
            order.status = 'cancelled'
        elif action == 'complete':
            # Change the order status to 'completed'
            order.status = 'completed'
        else:
            return JsonResponse({'success': False, 'error': 'Invalid action'}, status=400)        
        # Save the updated order status
        order.save()
        # Redirect back to the kitchen orders page
        return redirect(next_page)
    
    except Order.DoesNotExist:
        # Handle case where order_id doesn't exist
        return JsonResponse({'success': False, 'error': 'Order not found'}, status=404)


@login_required
def kitchen_menu(request):
    # Check if the user is kitchen staff
    if not request.user.is_kitchen:
        return redirect('restaurant_selection')
    
    if not request.user.managed_restaurant:
        return render(request, "kitchen/kitchen_menu.html", {
            "message": "No restaurant assigned to your account. Please contact admin.",
            "menu_items": []
        })
    
    menu_items = MenuItem.objects.filter(restaurant=request.user.managed_restaurant)
    return render(request, 'kitchen/kitchen_menu.html', {'menu_items': menu_items})

@login_required
@require_http_methods(["GET", "POST"])  # Allow both GET and POST requests
def edit_menu_item(request, item_id):
    if not request.user.is_kitchen:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    try:
        item = MenuItem.objects.get(id=item_id, restaurant=request.user.managed_restaurant)
        
        if request.method == "GET":
            # Return the item data as JSON
            data = {
                'id': item.id,
                'name': item.item_name,  # Changed from 'name' to match model field
                'price': str(item.price),
                'description': item.description if hasattr(item, 'description') else '',
                'image_url': item.image.url if item.image else None
            }
            print("Returning data:", data)  # Debug print
            return JsonResponse(data)

        elif request.method == "POST":
            try:
                # Parse the incoming data
                if request.content_type == 'application/json':
                    data = json.loads(request.body)
                else:
                    data = request.POST

                # Update the item fields
                if 'name' in data:
                    item.item_name = data['name']
                if 'price' in data:
                    item.price = data['price']
                if hasattr(item, 'description') and 'description' in data:
                    item.description = data['description']

                # Handle image upload
                if request.FILES and 'image' in request.FILES:
                    if item.image:
                        # Delete old image if it exists
                        try:
                            default_storage.delete(item.image.path)
                        except Exception as e:
                            print(f"Error deleting old image: {e}")
                    item.image = request.FILES['image']

                item.save()
                return JsonResponse({'success': True})

            except Exception as e:
                print(f"Error processing POST data: {e}")
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
            
    except MenuItem.DoesNotExist:
        return JsonResponse({
            'success': False, 
            'error': 'Item not found or not authorized'
        }, status=404)
    except Exception as e:
        print(f"Unexpected error in edit_menu_item: {e}")
        return JsonResponse({
            'success': False, 
            'error': str(e)
        }, status=500)

@login_required
@require_POST
def add_menu_item(request):
    if not request.user.is_kitchen:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    try:
        # Don't try to parse JSON since we're receiving FormData
        new_item = MenuItem.objects.create(
            restaurant=request.user.managed_restaurant,
            item_name=request.POST['name'],
            price=request.POST['price'],
            description=request.POST.get('description', ''),
        )
        
        if 'image' in request.FILES:
            new_item.image = request.FILES['image']
            new_item.save()
            
        return JsonResponse({'success': True, 'item_id': new_item.id})
    except Exception as e:
        print(f"Error adding menu item: {str(e)}")  # Add debug logging
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_POST
def delete_menu_item(request, item_id):
    if not request.user.is_kitchen:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    try:
        item = MenuItem.objects.get(id=item_id, restaurant=request.user.managed_restaurant)
        if item.image:
            default_storage.delete(item.image.path)
        item.delete()
        return JsonResponse({'success': True})
    except MenuItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'}, status=404)

# user login and register
# The login view now checks the user's is_kitchen status to determine where to redirect them,
# while the register view sets this status based on the user's selection during registration.
# ---------------------------------------------------------------------------------------
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            # Redirect based on user type
            if user.is_kitchen:
                return HttpResponseRedirect(reverse("kitchen_orders"))
            return HttpResponseRedirect(reverse("restaurant_selection"))
        else:
            return render(request, "orders/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "orders/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("restaurant_selection"))


def register(request):
    if request.method == "POST":
        email = request.POST["email"]
        user_type = request.POST.get("user_type", "customer")  # Get user type, default to customer

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "orders/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, email, password)
            user.is_kitchen = (user_type == "merchant")  # Set is_kitchen based on user type
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "orders/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        # Redirect based on user type
        if user.is_kitchen:
            return HttpResponseRedirect(reverse("kitchen_orders"))
        return HttpResponseRedirect(reverse("restaurant_selection"))
    else:
        return render(request, "orders/register.html")
    
