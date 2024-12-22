/**
 * Cart Management System
 * 
 * This module provides comprehensive functionality for managing a shopping cart
 * in a food ordering system. It handles real-time updates of cart contents,
 * prices, and quantities across both menu and cart pages.
 * 
 * Key Features:
 * - Real-time cart updates using AJAX
 * - Quantity management for menu items
 * - Price calculations and display
 * - Empty cart state handling
 * - Cross-page consistency between menu and cart views
 * 
 * Dependencies:
 * - util.js: For CSRF token management
 * - update_cart_total.js: For cart total calculations
 */

import { getCookie } from './util.js';
import { updateCartTotal } from './update_cart_total.js';


document.addEventListener('DOMContentLoaded', function() {
    // Initialize button event listeners
    initializeEventListeners();
    // Initial update of quantities
    updateItemQuantityDisplays();
});

/**
 * Initialize all event listeners for the page
 * Set up listeners for add and remove buttons in both menu and cart pages
 */
function initializeEventListeners() {
    // Select all add/remove buttons
    const addToOrderButtons = document.querySelectorAll('.add-to-order');
    const removeFromOrderButtons = document.querySelectorAll('.remove-from-order');

    // Add click handlers for 'add to order' buttons
    addToOrderButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.getAttribute('data-item-id');
            addItemToOrder(itemId);
        });
    });

    // Add click handlers for 'remove from order' buttons
    removeFromOrderButtons.forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.getAttribute('data-item-id');
            removeItemFromOrder(itemId);
        });
    });
}

/**
 * Add an item to the order
 * this function makes an AJAX call to the server to add the item to the order
 * @param {string} itemId - The ID of the item to add
 * @param {boolean} forceNew - Whether to force creation of new cart
 */
function addItemToOrder(itemId, forceNew = false) {
    fetch('/add-to-order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            item_id: itemId,
            force_new: forceNew
         })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateItemQuantityDisplays();
            updateCartTotal();
        } else if (data.error === 'different_restaurant') {
            console.log('Different restaurant detected:', data.message); // Debug log
            const userConfirmed = window.confirm(data.message);
            // Show confirmation dialog
            if (userConfirmed) {
                console.log('User confirmed, retrying with force_new=true'); // Debug log
                // If user confirms, call addItemToOrder again with force_new=true
                addItemToOrder(itemId, true);
            }
        }   
        else {
            alert('Failed to add item to order. ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
}

/**
 * Remove an item from the order
 * @param {string} itemId - The ID of the item to remove
 */
function removeItemFromOrder(itemId) {
    fetch('/remove-from-order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ item_id: itemId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateItemQuantityDisplays();
            updateCartTotal();
        } else {
            alert('Failed to remove item from order. ' + data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred. Please try again.');
    });
}

/**
 * Update the display of item quantities and prices throughout the page
 * Handles both menu page and cart page updates
 */
function updateItemQuantityDisplays() {
    console.log("Updating item quantities and displays");
    
    fetch('/get-item-quantities/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
    })
    .then(data => {
        if (data.success) {
            updateCartDisplay(data.quantities, data.total_prices);
        }
    })
    .catch(error => {
        console.error('Error in updateItemQuantityDisplays:', error);
    });
}

/**
 * Update the cart display with new quantities and prices
 * @param {Object} quantities - Dictionary of item quantities
 * @param {Object} totalPrices - Dictionary of item total prices
 */
function updateCartDisplay(quantities, totalPrices) {
    const cartItemRows = document.querySelectorAll('.cart-item-row');
    
    // Update cart items if we're on the cart page
    if (cartItemRows.length > 0) {
        cartItemRows.forEach(row => {
            const itemElement = row.querySelector('[data-item-id]');
            const itemId = itemElement.getAttribute('data-item-id');
            const quantity = quantities[itemId] || 0;

            // Handle visibility based on quantity
            if (quantity <= 0) {
                row.style.display = 'none';
            } else {
                row.style.display = 'grid';
                
                // Update quantity display
                const quantitySpan = row.querySelector('span.item-quantity');
                if (quantitySpan) quantitySpan.textContent = `x ${quantity}`;

                // Update price display
                const totalPriceElement = row.querySelector('.item-total-price');
                if (totalPriceElement) {
                    totalPriceElement.textContent = `$${totalPrices[itemId] || 0}`;
                }                
            }
        });

        // Handle empty cart state
        handleEmptyCartState(cartItemRows);
    } else {
        // Update menu page quantities
        updateMenuPageQuantities(quantities);
    }
}

/**
 * Handle the empty cart state
 * @param {NodeList} cartItemRows - All cart item rows
 */
function handleEmptyCartState(cartItemRows) {
    const visibleRows = Array.from(cartItemRows).filter(row => row.style.display !== 'none');
    const cartContainer = document.querySelector('.cart-items-container');
    const emptyCartMessage = document.querySelector('.empty-cart-message');
    
    if (visibleRows.length === 0) {
        if (cartContainer) cartContainer.style.display = 'none';
        if (emptyCartMessage) emptyCartMessage.style.display = 'block';
    } else {
        if (cartContainer) cartContainer.style.display = 'block';
        if (emptyCartMessage) emptyCartMessage.style.display = 'none';
    }
}

/**
 * Update quantities on the menu page
 * @param {Object} quantities - Dictionary of item quantities
 */
function updateMenuPageQuantities(quantities) {
    const quantitiesSpans = document.querySelectorAll('span.item-quantity[data-item-id]');
    quantitiesSpans.forEach(span => {
        const itemId = span.getAttribute('data-item-id');
        span.textContent = quantities[itemId] || 0;
    });
}