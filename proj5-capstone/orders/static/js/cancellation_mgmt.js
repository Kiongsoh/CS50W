/**
 * Cancellation Management Module
 * Handles the order cancellation UI and interactions, including modal display
 * and event handling for the cancellation process.
 */

import { getCookie } from './util.js';

export function showCancellationModal(orderId) {
    // Create and show Bootstrap modal
    // Main modal container with fade animation
    // Modal dialog - controls the width and margin of the modal
    // Modal content - contains the actual content of the modal
    // Modal header - contains title and close button
    // Modal body - contains the form for the cancellation reason and additional notes
    // Modal footer - contains action buttons
    const modalHtml = `
        <div class="modal fade" id="cancellationModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Cancel Order</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <form id="cancellationForm" method="POST" action="/kitchen/status/${orderId}/">
                            <input type="hidden" name="csrfmiddlewaretoken" value="${getCookie('csrftoken')}">
                            <input type="hidden" name="action" value="cancel">
                            <div class="mb-3">
                                <label for="cancellationReason" class="form-label">Reason for Cancellation</label>
                                <select class="form-select" id="cancellationReason" name="reason" required>
                                    <option value="unavailable">Items unavailable</option>
                                    <option value="customer">Customer canceled</option>
                                    <option value="closed">Store closed</option>
                                    <option value="busy">Store Busy</option>
                                    <option value="others">Others</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="additionalNotes" class="form-label">Additional Notes</label>
                                <textarea class="form-control" id="additionalNotes" name="notes" rows="3"></textarea>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="submit" class="btn btn-danger">Cancel Order</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    `;

    // Inject modal into DOM at end of body
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // Initialize and display Bootstrap modal
    const modal = new bootstrap.Modal(document.getElementById('cancellationModal'));
    modal.show();

    // Cleanup: Remove modal from DOM after it's hidden
    document.getElementById('cancellationModal').addEventListener('hidden.bs.modal', function () {
        this.remove();
    });
}

// Add click handlers to all cancel buttons
document.querySelectorAll('.cancel-order-btn').forEach(button => {
    button.addEventListener('click', function() {
        // This works because 'this' now refers to the button element
        const orderId = this.getAttribute('data-order-id');
        showCancellationModal(orderId);
    });
});