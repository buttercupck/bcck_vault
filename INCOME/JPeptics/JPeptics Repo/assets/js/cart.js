/*
 * Minimal Store Cart Logic
 *
 * This file contains all the necessary JavaScript for the client-side cart functionality.
 * It uses localStorage to persist the cart data between pages.
 */

document.addEventListener('DOMContentLoaded', () => {

    const cartKey = 'simpleStoreCart';

    // Helper function to get the cart from localStorage
    function getCart() {
        const cart = localStorage.getItem(cartKey);
        return cart ? JSON.parse(cart) : [];
    }

    // Helper function to save the cart to localStorage
    function saveCart(cart) {
        localStorage.setItem(cartKey, JSON.stringify(cart));
    }

    // --- Product Pages Logic ---
    const addToCartButton = document.querySelector('.add-to-cart-btn');
    if (addToCartButton) {
        addToCartButton.addEventListener('click', (e) => {
            const product = e.target.dataset;
            const cart = getCart();
            
            const existingProduct = cart.find(item => item.id === product.id);
            
            if (existingProduct) {
                existingProduct.quantity = parseInt(existingProduct.quantity) + 1;
            } else {
                cart.push({
                    id: product.id,
                    name: product.name,
                    price: parseFloat(product.price),
                    quantity: 1
                });
            }

            saveCart(cart);
            alert('Product added to cart!');
        });
    }

    // --- Cart Page Logic ---
    const cartTableBody = document.querySelector('.cart-table tbody');
    const updateCartButton = document.getElementById('update-cart-btn');
    const cartTotalElement = document.getElementById('cart-total');
    const checkoutButton = document.getElementById('checkout-btn');

    function renderCart() {
        if (!cartTableBody) return;

        const cart = getCart();
        cartTableBody.innerHTML = '';
        let total = 0;

        if (cart.length === 0) {
            cartTableBody.innerHTML = '<tr><td colspan="4">Your cart is empty.</td></tr>';
            cartTotalElement.textContent = '0.00';
            if (checkoutButton) {
                checkoutButton.disabled = true;
            }
            return;
        }

        if (checkoutButton) {
            checkoutButton.disabled = false;
        }

        cart.forEach((item, index) => {
            const row = document.createElement('tr');
            const lineTotal = item.price * item.quantity;
            total += lineTotal;

            row.innerHTML = `
                <td>${item.name}</td>
                <td>$${item.price.toFixed(2)}</td>
                <td>
                    <input type="number" value="${item.quantity}" min="1" data-id="${item.id}" class="quantity-input">
                </td>
                <td>$${lineTotal.toFixed(2)}</td>
                <td>
                    <button class="remove-btn" data-id="${item.id}">Remove</button>
                </td>
            `;
            cartTableBody.appendChild(row);
        });
        
        cartTotalElement.textContent = total.toFixed(2);
    }
    
    if (cartTableBody) {
        renderCart();

        cartTableBody.addEventListener('input', (e) => {
            if (e.target.classList.contains('quantity-input')) {
                const id = e.target.dataset.id;
                const newQuantity = parseInt(e.target.value);
                
                if (newQuantity < 1) return;

                const cart = getCart();
                const item = cart.find(i => i.id === id);
                if (item) {
                    item.quantity = newQuantity;
                    saveCart(cart);
                    renderCart();
                }
            }
        });

        cartTableBody.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-btn')) {
                const idToRemove = e.target.dataset.id;
                let cart = getCart();
                cart = cart.filter(item => item.id !== idToRemove);
                saveCart(cart);
                renderCart();
            }
        });
    }

    // --- Verify Page Logic ---
    const orderSummaryElement = document.getElementById('order-summary');
    const thankYouMessageElement = document.getElementById('thank-you-message');
    if (orderSummaryElement && thankYouMessageElement) {
        const cart = getCart();
        if (cart.length > 0) {
            let summaryHTML = '<h3>Order Summary</h3><ul>';
            let total = 0;
            cart.forEach(item => {
                const lineTotal = item.price * item.quantity;
                total += lineTotal;
                summaryHTML += `<li>${item.name} (x${item.quantity}): $${lineTotal.toFixed(2)}</li>`;
            });
            summaryHTML += `</ul><h4>Total: $${total.toFixed(2)}</h4>`;
            orderSummaryElement.innerHTML = summaryHTML;
            thankYouMessageElement.textContent = "Thank you for your order! Your payment details will be sent to your email shortly.";
        } else {
            thankYouMessageElement.textContent = "Thank you for visiting! Your cart was empty, but we hope to see you again soon.";
        }
        
        // Clear the cart after displaying the summary
        localStorage.removeItem(cartKey);
    }
});
