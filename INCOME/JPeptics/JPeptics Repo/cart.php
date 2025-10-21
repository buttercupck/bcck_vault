<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minimal Store - Cart</title>
    <meta name="description" content="View and manage your shopping cart. Update quantities or remove items before proceeding to checkout.">
    <link rel="canonical" href="https://yourdomain.com/cart.html">
    <link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>

    <header>
        <div class="logo-container">
            <a href="index.html">
                <img src="assets/img/logo.webp" alt="Minimal Store Logo">
            </a>
        </div>
        <nav class="main-nav">
            <ul>
                <li><a href="index.html">Home</a></li>
                <li class="product-nav-item">
                    <a href="#">Products</a>
                    <ul class="product-links">
                        <li><a href="product-1.html">Product One</a></li>
                        <li><a href="product-2.html">Product Two</a></li>
                        <li><a href="product-3.html">Product Three</a></li>
                    </ul>
                </li>
                <li><a href="cart.html" class="active">Cart</a></li>
                <li><a href="faq.html">FAQ</a></li>
                <li><a href="about.html">About</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <h1>Your Shopping Cart</h1>
        <table class="cart-table">
            <thead>
                <tr>
                    <th>Product</th>
                    <th>Price</th>
                    <th>Quantity</th>
                    <th>Total</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                <!-- Cart items will be rendered here by JS -->
            </tbody>
        </table>

        <div class="cart-totals">
            <p><strong>Subtotal:</strong> $<span id="cart-total">0.00</span></p>
        </div>

        <div class="cart-actions">
            <a href="index.html"><button>Continue Shopping</button></a>
            <a href="checkout.html"><button id="checkout-btn">Proceed to Checkout</button></a>
        </div>
    </main>

    <footer>
        <p>&copy; 2024 Minimal Store. All Rights Reserved.</p>
    </footer>

    <script src="assets/js/cart.js"></script>
</body>
</html>
