# Restaurant Ordering Web Application

A multi-restaurant platform that enables restaurants to create and manage their digital menu while allowing customers to discover and order from multiple restaurants in one place. The platform serves two main user groups:

- **For Restaurants**: Create and manage their digital menu, receive and process orders in real-time, and track order history - all through an intuitive kitchen interface.
- **For Customers**: Discover local restaurants, browse digital menus, place orders with customizations, and track order status through a seamless ordering experience.


## Distinctiveness and Complexity

This project stands out from other CS50W projects (including the old pizza project) in several ways:

1. **Multi-Restaurant Platform**: This application allows customers to browse and order from multiple restaurants in one place. Implements a marketplace model rather than a single-store model

2. **Dual-Role and Interface System**: Previous projects uses Admin-only menu management through Django Admin interface. This application provides a kitchen interface for restaurant staff to manage menus and handle orders. This is a new feature that is not present in the old pizza project:
   - Customer interface for browsing restaurants and ordering food
   - Kitchen interface for restaurant staff to manage menus and handle orders

3. **Menu Management**: The application allows restaurants to manage their menus (Create, Update, Delete) directly through a kitchen interface. This is a new feature that is not present in the old pizza project.

4. **Real-Time Updates**: The application implements real-time cart management and order status updates using AJAX:
   - Live cart quantity updates in the navigation bar
   - Dynamic price calculations
   - Complex order status workflow (incart → paid → accepted → completed/cancelled)
   - Immediate order status changes visible to both customers and kitchen staff
   - Order history for both customers and restaurants

5. **Complex Data Model**: The project uses a sophisticated database structure with multiple interconnected models:
   - User model with role-based access (customer/kitchen staff)
   - Restaurant model with associated menu items and categories
   - Order system with multiple status states and item quantities
   - Cancellation system with reason tracking

6. **Modern UI/UX Features**:
   - Responsive grid layouts for restaurants and menu items
   - Modal-based interactions for menu management
   - Dynamic cart updates without page reloads
   - Status badges and visual feedback for order states


## File Structure and Contents

### Backend (Python/Django)

- `models.py`: Defines database models for Users, Restaurants, Menu Items, Orders, and more
- `views.py`: Contains view functions for both customer and kitchen interfaces
- `urls.py`: URL routing configuration

### Frontend (JavaScript)

- `static/js/cart_management.js`: Handles all cart-related functionality
- `static/js/kitchen_menu.js`: Manages kitchen staff's menu editing interface
- `static/js/cancellation_mgmt.js`: Handles order cancellation workflow
- `static/js/update_cart_total.js`: Updates cart totals and quantities
- `static/js/util.js`: Utility functions used across the application

### Templates (HTML)

- `templates/orders/`:
  - `add_on_modal.html`: Modal template for customizing menu items with options like sweetness levels and special instructions
  - `cart.html`: Shopping cart page with real-time item management, quantity controls, and checkout options
  - `checkout.html`: Order checkout page
  - `history.html`: Detailed order history page showing past orders with timestamps, items, and status information
  - `menu_display.html`: Restaurant menu view
  - `order_confirmed.html`: Simple confirmation page displayed after successful order placement
  - `restaurant_selection.html`: Homepage with restaurant listings

- `templates/kitchen/`:
  - `kitchen_menu.html`: Menu management interface
  - `kitchen_orders.html`: Active orders view
  - `kitchen_history.html`: Order history view

## How to Run the Application

1. Ensure you have Python 3.8+ installed
2. Clone the repository
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```bash
   python manage.py runserver
   ```
8. Visit `http://127.0.0.1:8000/` in your browser

## Additional Information

- The application uses Django's built-in authentication system with custom user model
- Media files (restaurant and menu item images) are stored in the `media/` directory
- Static files are collected in the `static/` directory
- The project includes CSRF protection for all POST requests
- JavaScript modules are used for better code organization
- Bootstrap 5 is used for responsive design

## Requirements

See `requirements.txt` for a complete list of Python packages required. Key dependencies include:

- Django
- Pillow (for image handling)
- django-crispy-forms
- django-cleanup