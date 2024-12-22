# Restaurant Ordering Web Application

A comprehensive multi-restaurant platform that enables restaurants to create and manage their digital menus while allowing customers to discover and order from multiple restaurants in one place. The platform serves two main user groups:

- **For Restaurants**: Create and manage their digital menus, receive and process orders in real-time, and track order history - all through an intuitive kitchen interface.
- **For Customers**: Discover local restaurants, browse digital menus, place orders with customizations, and track order status through a seamless ordering experience.

## Distinctiveness and Complexity

This project stands out from other CS50W projects in several ways:

1. **Multi-Restaurant Platform**: Unlike single-restaurant systems, this application:
   - Allows multiple restaurants to self-register and manage their presence
   - Provides a marketplace for customers to discover and order from various restaurants
   - Maintains separate menu management and order processing for each restaurant

2. **Real-Time Updates**: The application implements real-time cart management and order status updates using AJAX:
   - Live cart quantity updates in the navigation bar
   - Dynamic price calculations
   - Immediate order status changes visible to both customers and kitchen staff
   - Real-time menu availability updates

3. **Complex Data Model**: The project uses a database structure with multiple interconnected models:
   - User model with role-based access (customer/kitchen staff)
   - Restaurant model with associated menu items and categories
   - Order system with multiple status states and item quantities
   - Cancellation system with reason tracking

4. **Modern UI/UX Features**:
   - Responsive grid layouts for restaurants and menu items
   - Modal-based interactions for menu management
   - Dynamic cart updates without page reloads
   - Status badges and visual feedback for order states
   - Customizable menu items with add-on options

## Key Differences from Single-Restaurant Systems

This project significantly expands upon traditional single-restaurant ordering systems in several ways:

1. **Restaurant Management**:
   - Custom kitchen interface instead of Django Admin
   - Real-time menu management with image uploads
   - Restaurant-specific dashboards and analytics
   - Support for restaurant chains and branches

2. **Advanced Order Processing**:
   - Sophisticated order status workflow
   - Real-time order tracking and updates
   - Detailed cancellation system with reason tracking
   - Separate order queues per restaurant
   - Comprehensive order history for both parties

3. **User Roles and Permissions**:
   - Dual interface system (customer/kitchen)
   - Restaurant-staff associations
   - Role-based access control
   - Restaurant-specific permissions

4. **Technical Enhancements**:
   - AJAX-powered real-time updates
   - Modular JavaScript architecture
   - Dynamic cart management
   - Modal-based interactions
   - Real-time calculations and updates

5. **Scalable Data Model for future development**:
   - Support for restaurant chains
   - Menu categorization
   - Rating and review system
   - Operating hours management

### Templates (HTML)

- `templates/orders/` (Customer Interface):
  - `restaurant_selection.html`: Homepage featuring:
    * Restaurant grid display
    * Rating and cuisine information
    * Operating hours
    * Restaurant images
    * Promotional content section

  - `menu_display.html`: Restaurant menu page with:
    * Menu item grid layout
    * Item images and descriptions
    * Price display
    * Quantity controls
    * Dynamic cart integration

  - `checkout.html`: Checkout interface including:
    * Order summary
    * Item quantities and prices
    * Total calculation

    * Payment form
    * Order confirmation

  - `cart.html`: Shopping cart page with real-time item management, quantity controls, and checkout options

  - `add_on_modal.html`: Modal template for customizing menu items with options like sweetness levels and special instructions

  - `order_confirmed.html`: Simple confirmation page displayed after successful order placement

  - `history.html`: Detailed order history page showing past orders with timestamps, items, and status information

- `templates/kitchen/` (Kitchen Staff Interface):
  - `kitchen_menu.html`: Menu management page with:
    * Current menu item display
    * Add/Edit/Delete controls
    * Image upload interface
    * Modal forms for item management
    * Real-time updates

  - `kitchen_orders.html`: Active orders dashboard:
    * New and in-progress orders
    * Order details and items
    * Status management controls
    * Cancellation interface
    * Customer information

  - `kitchen_history.html`: Order history view with:
    * Complete order history
    * Filtering and sorting options
    * Status tracking
    * Order details
    * Cancellation records

// ... rest of the file ... 