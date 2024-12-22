/**
 * Cart Total Update Module
 * Updates the cart total and quantity display
 * Makes an AJAX call to get current cart data and updates the DOM
 */

import { getCookie } from './util.js';

// Log when the script starts loading
console.log("update_cart_total.js loaded");

export function updateCartTotal() {
    console.log("updateCartTotal function called");
    
    // Make a GET request to the server to retrieve the cart data
    fetch('/get-cart-quantity/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for security
        }
    })
    .then(response => {
        console.log("Response status:", response.status);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Cart quantity data received:", data);
        
        // update cart quantity display in navbar
        const cartQuantityElement = document.getElementById('cart-quantity');
                
        if (cartQuantityElement) {
            // Update the cart quantity in the DOM
            if (data.quantity > 0) {
                cartQuantityElement.textContent = data.quantity;
                cartQuantityElement.style.display = 'inline';
            } else {
                cartQuantityElement.textContent = '';
                cartQuantityElement.style.display = 'none';
            }
            console.log("Cart quantity updated:", data.quantity);
        } else {
            console.error("Cart quantity element not found in the DOM");
        }

        // -----------------------------------------------------------------
        // update total bill $ display in cart page
        const totalBillElement = document.querySelector('.total-amount');

        if (totalBillElement) {
            // Update total bill display
            const totalPrice = parseFloat(data.total_price);
            totalBillElement.textContent = `S$ ${totalPrice.toFixed(2)}`;
        }
    })
    .catch(error => {
        console.error('Error in updateCartTotal:', error);
    });
}

/**
 * Initializes the cart quantity update functionality
 * Sets up initial update and periodic updates
 */
function initializeCartQuantity() {
    console.log("initializeCartQuantity function called");
    
    // Check if the cart quantity element exists in the DOM
    const cartQuantityElement = document.getElementById('cart-quantity');
    
    if (cartQuantityElement) {
        console.log("Cart quantity element found, initializing...");
        // Update the cart quantity immediately
        updateCartTotal();
        // Set up an interval to update the cart quantity every 30 seconds
        setInterval(updateCartTotal, 30000);
    } else {
        console.error("Cart quantity element not found on page load");
    }
}

// Add an event listener for when the DOM content is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the cart quantity when the DOM is ready
    initializeCartQuantity();
});

// Log when the script finishes loading
console.log("cart_quantity.js finished loading");