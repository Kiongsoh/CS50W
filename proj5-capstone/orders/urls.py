from django.urls import path
from . import views

urlpatterns = [
    path('', views.restaurant_selection, name='restaurant_selection'),
    path('restaurant/<int:restaurant_id>/', views.menu_display, name='menu_display'),
    path('add-to-order/', views.add_to_order, name='add_to_order'),
    path('remove-from-order/', views.remove_from_order, name='remove_from_order'),
    path('cart/', views.view_cart, name='view_cart'),
    path('get-cart-quantity/', views.get_cart_quantity, name='get_cart_quantity'), # this route is used to get the total cart quantity in the navbar
    path('get-item-quantities/', views.get_item_quantities, name='get_item_quantities'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmed/', views.order_confirmed, name='order_confirmed'),
    path('history/', views.history, name='history'),

    path('kitchen/', views.kitchen_orders, name='kitchen_orders'),
    path('kitchen/history/', views.kitchen_history, name='kitchen_history'),
    path('kitchen/status/<int:order_id>/', views.update_status, name='update_status'),

    path('kitchen/menu/', views.kitchen_menu, name='kitchen_menu'),
    path('kitchen/menu/edit/<int:item_id>/', views.edit_menu_item, name='edit_menu_item'),
    path('kitchen/menu/add/', views.add_menu_item, name='add_menu_item'),
    path('kitchen/menu/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]
