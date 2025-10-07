<?php
// Get order data from form submission or session
$product = $_POST['product'] ?? 'tirzepatide';
$package_size = $_POST['package_size'] ?? '3-pack-179';
$quantity = $_POST['quantity'] ?? '1';

// Parse package info
$package_parts = explode('-', $package_size);
$pack_count = $package_parts[0] ?? '3';
$price = $package_parts[2] ?? '179';

// Generate order number (date-based as specified in plan)
$order_number = 'JP-' . date('Y') . '-' . sprintf('%03d', rand(1, 999));

// Calculate Bitcoin amount (example conversion, would be dynamic in real implementation)
$btc_amount = number_format($price / 59500, 8); // Example BTC price

$confirmation_submitted = isset($_POST['transaction_id']) && !empty($_POST['transaction_id']);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Your Payment - JPeptics</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,300;1,400;1,500;1,700&family=Source+Sans+Pro:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600&display=swap');
        
        :root {
            --primary-blue: #428ce0;
            --primary-blue-dark: #3574c4;
            --primary-blue-light: #5fa3e8;
            --primary-blue-pale: #e8f2fd;
            --primary-magenta: #e344aa;
            --primary-magenta-dark: #cc3d9a;
            --secondary-green: #10B981;
            --success: #22C55E;
            --warning: #F59E0B;
            --danger: #EF4444;
            --white: #FFFFFF;
            --gray-50: #FAFAFA;
            --gray-100: #F5F5F5;
            --gray-200: #E5E5E5;
            --gray-600: #525252;
            --gray-700: #404040;
            --gray-800: #262626;
            --gray-900: #171717;
            --font-primary: 'Roboto', sans-serif;
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --radius-lg: 0.75rem;
            --radius-xl: 1rem;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: var(--font-primary);
            background-color: var(--gray-50);
            color: var(--gray-700);
            line-height: 1.6;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 1.5rem;
        }

        /* Header */
        .header {
            background: var(--white);
            box-shadow: var(--shadow-md);
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
        }

        .logo {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--primary-blue);
        }

        .nav-links {
            display: flex;
            gap: 2rem;
            list-style: none;
        }

        .nav-link {
            color: var(--gray-600);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s;
        }

        .nav-link:hover {
            color: var(--primary-blue);
        }

        .btn {
            padding: 0.75rem 1.5rem;
            border-radius: var(--radius-lg);
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
            display: inline-block;
            text-align: center;
        }

        .btn-primary {
            background: var(--primary-blue);
            color: var(--white);
        }

        .btn-primary:hover {
            background: var(--primary-blue-dark);
            transform: translateY(-1px);
        }

        .btn-lg {
            padding: 1rem 2rem;
            font-size: 1.125rem;
        }

        /* Section Styles */
        .section {
            padding: 3rem 0;
        }

        .section-title {
            font-size: 2.5rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 3rem;
            color: var(--gray-800);
        }

        /* Payment Container */
        .payment-container {
            max-width: 700px;
            margin: 0 auto;
        }

        .payment-section {
            background: var(--white);
            border-radius: var(--radius-xl);
            padding: 2.5rem;
            box-shadow: var(--shadow-md);
            margin-bottom: 2rem;
        }

        .section-header {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--gray-800);
            margin-bottom: 1.5rem;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid var(--gray-200);
        }

        /* Order Summary */
        .order-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
            border-bottom: 1px solid var(--gray-200);
        }

        .order-item:last-child {
            border-bottom: 2px solid var(--gray-800);
            font-weight: 600;
            font-size: 1.1rem;
        }

        /* Bitcoin Address */
        .bitcoin-address {
            background: var(--gray-100);
            border: 2px solid var(--primary-blue-light);
            border-radius: var(--radius-lg);
            padding: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: monospace;
            word-break: break-all;
        }

        .copy-btn {
            background: var(--primary-blue);
            color: var(--white);
            border: none;
            padding: 0.5rem 1rem;
            border-radius: var(--radius-lg);
            cursor: pointer;
            margin-left: 1rem;
            flex-shrink: 0;
        }

        /* Form Styles */
        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-label {
            display: block;
            font-weight: 500;
            margin-bottom: 0.5rem;
            color: var(--gray-700);
        }

        .form-input {
            width: 100%;
            padding: 0.75rem;
            border: 2px solid var(--gray-200);
            border-radius: var(--radius-lg);
            font-size: 1rem;
            transition: border-color 0.2s;
            font-family: var(--font-primary);
        }

        .form-input:focus {
            outline: none;
            border-color: var(--primary-blue);
        }

        .form-input[readonly] {
            background: var(--gray-100);
            font-family: monospace;
        }

        /* Warning Box */
        .warning-box {
            background: #FEF3C7;
            border: 2px solid var(--warning);
            border-radius: var(--radius-lg);
            padding: 1rem;
            margin: 1.5rem 0;
            display: flex;
            align-items: center;
        }

        .warning-box::before {
            content: "⚠️";
            margin-right: 0.75rem;
            font-size: 1.25rem;
        }

        /* Order Confirmation */
        .order-confirmation {
            background: var(--secondary-green);
            color: var(--white);
            border-radius: var(--radius-xl);
            padding: 2.5rem;
            text-align: center;
            margin: 2rem 0;
        }

        .confirmation-details {
            background: rgba(255,255,255,0.2);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            margin: 1.5rem 0;
            text-align: left;
        }

        .confirmation-details h4 {
            margin-bottom: 1rem;
        }

        .confirmation-details p {
            margin-bottom: 0.5rem;
        }

        .next-steps {
            background: rgba(255,255,255,0.2);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            margin: 1.5rem 0;
            text-align: left;
        }

        .next-steps h4 {
            margin-bottom: 1rem;
        }

        .step-item {
            display: flex;
            align-items: center;
            margin-bottom: 0.5rem;
        }

        .step-item::before {
            content: "✓";
            color: var(--white);
            font-weight: bold;
            margin-right: 0.75rem;
            font-size: 1.1rem;
        }

        @media (max-width: 768px) {
            .nav-links { display: none; }
            .payment-section { padding: 1.5rem; }
            .bitcoin-address { flex-direction: column; }
            .copy-btn { margin-left: 0; margin-top: 1rem; }
            .order-item { flex-direction: column; align-items: flex-start; }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <nav class="nav">
                <div class="logo">JPeptics</div>
                <ul class="nav-links">
                    <li><a href="index.php" class="nav-link">Home</a></li>
                    <li><a href="products-page.php" class="nav-link">Products</a></li>
                    <li><a href="#" class="nav-link">Support</a></li>
                </ul>
                <a href="order-form.php" class="btn btn-primary">Order Now</a>
            </nav>
        </div>
    </header>

    <!-- Payment Verification Section -->
    <section class="section">
        <div class="container">
            <?php if (!$confirmation_submitted): ?>
                <h2 class="section-title">✅ Complete Your Bitcoin Payment</h2>
                
                <div class="payment-container">
                    <!-- Order Summary -->
                    <div class="payment-section">
                        <h3 class="section-header">Order Summary</h3>
                        <div class="order-item">
                            <span>1x <?= ucfirst($product) ?> <?= $pack_count ?> pack</span>
                            <span>$<?= $price ?></span>
                        </div>
                        <div class="order-item">
                            <span>Shipping</span>
                            <span>FREE</span>
                        </div>
                        <div class="order-item">
                            <span><strong>Total</strong></span>
                            <span><strong>$<?= $price ?></strong></span>
                        </div>
                    </div>

                    <!-- Bitcoin Payment Address -->
                    <div class="payment-section">
                        <h3 class="section-header">Bitcoin Payment Address</h3>
                        <div class="bitcoin-address">
                            <span>bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh</span>
                            <button class="copy-btn" onclick="copyAddress()">Copy 📋</button>
                        </div>
                        <p style="margin-top: 1rem; color: var(--gray-600); font-size: 0.9rem;">
                            <strong>Amount to Send:</strong> <?= $btc_amount ?> BTC ($<?= $price ?>)
                        </p>
                    </div>

                    <!-- Transaction ID Submission -->
                    <div class="payment-section">
                        <h3 class="section-header">Transaction ID Submission</h3>
                        
                        <form method="POST" action="">
                            <input type="hidden" name="product" value="<?= htmlspecialchars($product) ?>">
                            <input type="hidden" name="package_size" value="<?= htmlspecialchars($package_size) ?>">
                            <input type="hidden" name="quantity" value="<?= htmlspecialchars($quantity) ?>">
                            <input type="hidden" name="order_number" value="<?= $order_number ?>">
                            <input type="hidden" name="price" value="<?= $price ?>">
                            
                            <div class="form-group">
                                <label class="form-label">Bitcoin Transaction ID (Hash)</label>
                                <input type="text" name="transaction_id" class="form-input" placeholder="Enter your transaction ID from CashApp" style="font-family: monospace;" required>
                                <small style="color: var(--gray-600); margin-top: 0.5rem; display: block;">This is a long string of letters and numbers provided by CashApp after sending Bitcoin</small>
                            </div>

                            <div class="form-group">
                                <label class="form-label">Order Email</label>
                                <input type="email" name="order_email" class="form-input" placeholder="Email for order confirmation" required>
                            </div>

                            <div class="form-group">
                                <label class="form-label">Amount Sent (USD)</label>
                                <input type="number" name="amount_sent" class="form-input" value="<?= $price ?>" step="0.01" readonly>
                            </div>

                            <div class="warning-box">
                                <span><strong>Important:</strong> Send exact amount to avoid delays in processing your order.</span>
                            </div>

                            <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;">Submit Transaction</button>
                        </form>
                    </div>

                    <!-- After Submission Info -->
                    <div class="payment-section">
                        <h3 class="section-header">After submission:</h3>
                        <ul style="list-style: none; margin-left: 0;">
                            <li style="margin-bottom: 0.5rem;">• We'll verify your payment (1-6 hours)</li>
                            <li style="margin-bottom: 0.5rem;">• You'll receive email confirmation</li>
                            <li style="margin-bottom: 0.5rem;">• Order ships within 1-2 business days</li>
                        </ul>
                    </div>
                </div>

            <?php else: ?>
                <!-- Order Confirmation (shown after submission) -->
                <div class="order-confirmation">
                    <h3>🎉 Order Confirmed!</h3>
                    <p style="margin: 1rem 0;">Thank you for your order! We've received your Bitcoin transaction and are processing your order.</p>
                    
                    <div class="confirmation-details">
                        <h4>Order Details:</h4>
                        <p><strong>Order #:</strong> <?= $order_number ?></p>
                        <p><strong>Product:</strong> <?= ucfirst($product) ?> <?= $pack_count ?>-pack</p>
                        <p><strong>Amount:</strong> $<?= $price ?></p>
                        <p><strong>Transaction ID:</strong> <?= substr($_POST['transaction_id'], 0, 12) ?>...<?= substr($_POST['transaction_id'], -8) ?></p>
                        <p><strong>Status:</strong> Processing</p>
                        <p><strong>Email:</strong> <?= htmlspecialchars($_POST['order_email']) ?></p>
                    </div>

                    <div class="next-steps">
                        <h4>What Happens Next:</h4>
                        <div class="step-item">You'll receive email confirmation within 15 minutes</div>
                        <div class="step-item">Order ships within 1-2 business days</div>
                        <div class="step-item">Tracking information will be sent via email</div>
                        <div class="step-item">Package arrives in discreet packaging</div>
                    </div>

                    <p style="margin-top: 2rem;">Questions? Contact us at <strong>JPeptics@gmail.com</strong></p>
                </div>

                <?php
                // Send email notification to JPeptics@gmail.com (in real implementation)
                // This would include all order details and transaction ID
                ?>

            <?php endif; ?>
        </div>
    </section>

    <script>
        function copyAddress() {
            const address = 'bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh';
            navigator.clipboard.writeText(address).then(function() {
                alert('Bitcoin address copied to clipboard!');
            });
        }
    </script>
</body>
</html>