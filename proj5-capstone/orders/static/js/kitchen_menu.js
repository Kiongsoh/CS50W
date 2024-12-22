// Import the getCookie utility function from util.js
// This is used to get the CSRF token for secure form submissions
import { getCookie } from './util.js';

// Wait for the DOM to be fully loaded before executing any code
document.addEventListener('DOMContentLoaded', function() {
    // Get the CSRF token from cookies - required for Django form submissions
    const csrfToken = getCookie('csrftoken');
    
    // === Event Listeners Setup ===
    
    // Add click handler for the "Add New Item" button
    // When clicked, it shows the modal with empty fields
    document.getElementById('addItemBtn').addEventListener('click', () => showModal());
    
    // Add click handler for the "Save" button in the modal
    // This will trigger the item save/update process
    document.getElementById('saveItemBtn').addEventListener('click', saveItem);
    
    // Add click handlers to all "Edit" buttons in the menu grid
    // Uses event delegation to handle dynamically added elements
    document.querySelectorAll('.edit-item-btn').forEach(btn => {
        btn.addEventListener('click', (e) => editItem(e.target.dataset.itemId));
    });
    
    // Add click handlers to all "Delete" buttons in the menu grid
    document.querySelectorAll('.delete-item-btn').forEach(btn => {
        btn.addEventListener('click', (e) => deleteItem(e.target.dataset.itemId));
    });
    
    // === Modal Management Function ===
    
    /**
     * Shows the modal for adding/editing items
     * @param {Object|null} itemData - Data of the item being edited, null for new items
     */
    function showModal(itemData = null) {
        const modal = document.getElementById('itemModal');
        const form = document.getElementById('itemForm');
        
        // Clear any existing data in the form
        form.reset();
        
        // Set the item ID (empty for new items)
        // if itemData exists, set the itemId to the itemData.id
        // otherwise, set it to an empty string
        document.getElementById('itemId').value = itemData ? itemData.id : '';
        
        // If editing an existing item, populate the form fields
        if (itemData) {
            document.getElementById('itemName').value = itemData.name;
            document.getElementById('itemPrice').value = itemData.price;
            document.getElementById('itemDescription').value = itemData.description;
        }
        
        // Show the modal using Bootstrap 5's modal API
        const bsModal = new bootstrap.Modal(modal);
        bsModal.show();
    }
    
    // === CRUD Operations ===
    
    /**
     * Saves or updates a menu item
     * Uses FormData to handle file uploads along with regular data
     */
    async function saveItem() {
        const itemId = document.getElementById('itemId').value;
        const formData = new FormData();
        
        // Gather form data
        formData.append('name', document.getElementById('itemName').value);
        formData.append('price', document.getElementById('itemPrice').value);
        formData.append('description', document.getElementById('itemDescription').value);
        
        // Handle image file if one was selected
        const imageFile = document.getElementById('itemImage').files[0];
        if (imageFile) {
            formData.append('image', imageFile);
        }
        
        try {
            // Determine if we're creating new or updating existing
            const url = itemId ? 
                `/kitchen/menu/edit/${itemId}/` : 
                '/kitchen/menu/add/';
                
            // Send the request to the server
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken, // Required for Django's CSRF protection
                },
                body: formData
            });
            
            if (response.ok) {
                location.reload(); // Refresh page to show changes
            } else {
                alert('Error saving item');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error saving item');
        }
    }
    
    /**
     * Loads item data for editing
     * @param {string} itemId - ID of the item to edit
     */
    async function editItem(itemId) {
        try {
            // Fetch the current item data from the server
            const response = await fetch(`/kitchen/menu/edit/${itemId}/`);
            const data = await response.json();
            // Show the modal with the item data
            showModal(data);
        } catch (error) {
            console.error('Error:', error);
            alert('Error loading item data');
        }
    }
    
    /**
     * Deletes a menu item
     * @param {string} itemId - ID of the item to delete
     */
    async function deleteItem(itemId) {
        // Show confirmation dialog before deleting
        if (!confirm('Are you sure you want to delete this item?')) {
            return;
        }
        
        try {
            // Send delete request to the server
            const response = await fetch(`/kitchen/menu/delete/${itemId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken, // Required for Django's CSRF protection
                }
            });
            
            if (response.ok) {
                location.reload(); // Refresh page to show changes
            } else {
                alert('Error deleting item');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error deleting item');
        }
    }
});