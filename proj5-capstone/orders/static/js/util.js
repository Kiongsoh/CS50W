// Utility functions shared across multiple JavaScript files

/**
 * Function to retrieve a cookie value by name
 * @param {string} name - The name of the cookie to retrieve
 * @return {string|null} The cookie value if found, null otherwise
 */
function getCookie(name) {
    // Initialize cookieValue as null
    let cookieValue = null;
    
    // Check if document.cookie exists and is not an empty string
    if (document.cookie && document.cookie !== '') {
        // Split the cookie string into an array of individual cookies
        const cookies = document.cookie.split(';');
        
        // Iterate through each cookie
        for (let i = 0; i < cookies.length; i++) {
            // Remove whitespace from the beginning and end of the cookie string
            const cookie = cookies[i].trim();
            
            // Check if this cookie string begins with the name we want
            // The '+1' accounts for the '=' sign after the cookie name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                // If found, decode and store the cookie value
                // substring(name.length + 1) removes the cookie name and '=' from the string
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                // Exit the loop as we've found the cookie we're looking for
                break;
            }
        }
    }
    
    // Return the cookie value (or null if not found)
    return cookieValue;
}

// Export the function so it can be imported in other files
// This allows us to use ES6 module syntax in other JavaScript files
export { getCookie };