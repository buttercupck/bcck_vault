<?php
// Get product data from POST or GET parameters
$product = $_POST['product'] ?? $_GET['product'] ?? '';
$package_size = $_POST['package_size'] ?? $_GET['package_size'] ?? '';
$quantity = $_POST['quantity'] ?? $_GET['quantity'] ?? '1';

// Parse package information
if ($package_size) {
    $package_parts = explode('-', $package_size);
    $pack_count = $package_parts[0] ?? '';
    $price = $package_parts[2] ?? '';
} else {
    $pack_count = '';
    $price = '';
}

// Product display names
$product_names = [
    'tirzepatide' => 'Tirzepatide',
    'retatrutide' => 'Retatrutide'
];

$product_display = $product_names[$product] ?? '';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['payment_method'])) {
    $payment_method = $_POST['payment_method'];
    $full_name = $_POST['full_name'] ?? '';
    $email = $_POST['email'] ?? '';
    $phone = $_POST['phone'] ?? '';
    $street_address = $_POST['street_address'] ?? '';
    $address_line_2 = $_POST['address_line_2'] ?? '';
    $city = $_POST['city'] ?? '';
    $state = $_POST['state'] ?? '';
    $zip_code = $_POST['zip_code'] ?? '';
    $country = $_POST['country'] ?? '';
    
    // Generate order number (date-based as specified in plan)
    $order_number = 'JP-' . date('Y') . '-' . sprintf('%03d', rand(1, 999));
    
    // Prepare email content
    $to = 'JPeptics@gmail.com';
    $subject = "New Order Received - Order #$order_number";
    
    $message = "
    New order received on JPeptics website:
    
    ORDER DETAILS:
    Order Number: $order_number
    Date: " . date('Y-m-d H:i:s') . "
    
    PRODUCT SELECTION:
    Product: $product_display
    Package: $pack_count pack
    Price: $price
    Quantity: $quantity
    Payment Method: " . ucfirst($payment_method) . "
    
    CUSTOMER INFORMATION:
    Name: $full_name
    Email: $email
    Phone: $phone
    
    SHIPPING ADDRESS:
    $street_address
    " . ($address_line_2 ? "$address_line_2\n    " : "") . "$city, $state $zip_code
    $country
    
    ---
    This is an automated message from the JPeptics order system.
    ";
    
    $headers = "From: orders@jpeptics.com\r\n";
    $headers .= "Reply-To: $email\r\n";
    $headers .= "X-Mailer: PHP/" . phpversion();
    
    // Send email notification
    $email_sent = mail($to, $subject, $message, $headers);
    
    // Redirect based on payment method
    if ($payment_method === 'bitcoin') {
        // Store order data in session for the payment page
        session_start();
        $_SESSION['order_data'] = [
            'order_number' => $order_number,
            'product' => $product,
            'package_size' => $package_size,
            'quantity' => $quantity,
            'price' => $price,
            'customer_info' => [
                'name' => $full_name,
                'email' => $email,
                'phone' => $phone,
                'address' => "$street_address, $city, $state $zip_code"
            ]
        ];
        header('Location: btc-payment-info.php');
        exit;
    } else {
        header('Location: other-payments-page.php');
        exit;
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Complete Your Order - JPeptics</title>
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

        /* Form Styles */
        .order-form {
            background: var(--white);
            border-radius: var(--radius-xl);
            padding: 3rem;
            box-shadow: var(--shadow-md);
            max-width: 700px;
            margin: 0 auto;
        }

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

        .select-input {
            background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
            background-position: right 0.75rem center;
            background-repeat: no-repeat;
            background-size: 1.5em 1.5em;
            padding-right: 2.5rem;
            appearance: none;
        }

        .form-section {
            border-bottom: 1px solid var(--gray-200);
            padding-bottom: 2rem;
            margin-bottom: 2rem;
        }

        .form-section:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }

        .form-section h3 {
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--gray-800);
            margin-bottom: 1.5rem;
        }

        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }

        /* Order Summary Styles */
        .order-summary {
            background: var(--white);
            border-radius: var(--radius-xl);
            padding: 3rem;
            box-shadow: var(--shadow-md);
            margin-bottom: 2rem;
            border-left: 4px solid var(--primary-blue);
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }

        .order-summary.tirzepatide {
            border-left-color: var(--primary-magenta);
        }

        .order-summary h3 {
            color: var(--primary-blue);
            margin-bottom: 1.5rem;
        }

        .order-summary.tirzepatide h3 {
            color: var(--primary-magenta);
        }

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

        .edit-link {
            color: var(--primary-blue);
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
        }

        .edit-link:hover {
            text-decoration: underline;
        }

        .product-selection {
            background: var(--primary-blue-pale);
            border-radius: var(--radius-xl);
            padding: 2rem;
            margin-bottom: 2rem;
            text-align: center;
        }

        .product-selection h3 {
            color: var(--primary-blue);
            margin-bottom: 1rem;
        }

        .product-selection p {
            color: var(--gray-600);
            margin-bottom: 1.5rem;
        }

        .payment-buttons {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-top: 1rem;
        }

        .payment-btn {
            padding: 1rem 2rem;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: var(--radius-lg);
            transition: all 0.2s;
            cursor: pointer;
            border: 2px solid transparent;
        }

        .payment-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .required {
            color: var(--danger);
        }

        @media (max-width: 768px) {
            .nav-links { display: none; }
            .grid-2 { grid-template-columns: 1fr; }
            .order-form { padding: 2rem; margin: 0 1rem; }
            .order-summary { margin: 0 1rem 2rem 1rem; }
            .product-selection { margin: 0 1rem 2rem 1rem; }
            .payment-buttons { grid-template-columns: 1fr; }
            .payment-btn { padding: 1rem 1.5rem; font-size: 1rem; }
        }

        @media (max-width: 768px) {
            .nav-links { display: none; }
            .grid-2 { grid-template-columns: 1fr; }
            .order-form { padding: 2rem; margin: 0 1rem; }
            .order-summary { margin: 0 1rem 2rem 1rem; }
            .product-selection { margin: 0 1rem 2rem 1rem; }
        }
    </style>
</head>
<body>
    <!-- Header -->
   <?php include 'partials/header.php'; ?>

    <!-- Order Form Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">Complete Your Order</h2>
            
            <?php if ($product && $package_size): ?>
                <!-- Order Summary -->
                <div class="order-summary <?php echo $product; ?>">
                    <h3>Your Selection</h3>
                    <div class="order-item">
                        <span><?php echo $quantity; ?>x <?php echo $product_display; ?> <?php echo $pack_count; ?> pack</span>
                        <span>$<?php echo $price; ?></span>
                    </div>
                    <div class="order-item">
                        <span>Shipping</span>
                        <span>$5</span>
                    </div>
                    <div class="order-item">
                        <span><strong>Total</strong></span>
                        <span><strong>$<?php echo $price; ?></strong></span>
                    </div>
                    <div style="text-align: center; margin-top: 1rem;">
                        <a href="<?php echo $product === 'tirzepatide' ? 'tz' : 'rz'; ?>-product-page.php" class="edit-link">← Change Product Selection</a>
                    </div>
                </div>
            <?php else: ?>
                <!-- No Product Selected -->
                <div class="product-selection">
                    <h3>No Product Selected</h3>
                    <p>Please select a product and package size to continue with your order.</p>
                    <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                        <a href="tz-product-page.php" class="btn btn-primary">Shop Tirzepatide</a>
                        <a href="rz-product-page.php" class="btn btn-primary">Shop Retatrutide</a>
                    </div>
                </div>
            <?php endif; ?>
            
            <form class="order-form" method="POST" action="">
                <!-- Hidden Fields to Preserve Selection -->
                <input type="hidden" name="product" value="<?php echo htmlspecialchars($product); ?>">
                <input type="hidden" name="package_size" value="<?php echo htmlspecialchars($package_size); ?>">
                <input type="hidden" name="quantity" value="<?php echo htmlspecialchars($quantity); ?>">
                <input type="hidden" name="price" value="<?php echo htmlspecialchars($price); ?>">
                
                <!-- Customer Information -->
                <div class="form-section">
                    <h3>Customer Information</h3>
                    <div class="form-group">
                        <label class="form-label">Full Name <span class="required">*</span></label>
                        <input type="text" name="full_name" class="form-input" placeholder="Enter your full name" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Email Address <span class="required">*</span></label>
                        <input type="email" name="email" class="form-input" placeholder="your@email.com" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Phone Number <span class="required">*</span></label>
                        <input type="tel" name="phone" class="form-input" placeholder="(555) 123-4567" required>
                    </div>
                </div>

                <!-- Shipping Address -->
                <div class="form-section">
                    <h3>Shipping Address</h3>
                    <div class="form-group">
                        <label class="form-label">Street Address <span class="required">*</span></label>
                        <input type="text" name="street_address" class="form-input" placeholder="123 Main Street" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Address Line 2</label>
                        <input type="text" name="address_line_2" class="form-input" placeholder="Apartment, suite, etc. (optional)">
                    </div>
                    <div class="grid-2">
                        <div class="form-group">
                            <label class="form-label">City <span class="required">*</span></label>
                            <input type="text" name="city" class="form-input" placeholder="City" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">State <span class="required">*</span></label>
                            <input type="text" name="state" class="form-input" placeholder="State" required>
                        </div>
                    </div>
                    <div class="grid-2">
                        <div class="form-group">
                            <label class="form-label">ZIP Code <span class="required">*</span></label>
                            <input type="text" name="zip_code" class="form-input" placeholder="12345" required>
                        </div>
                        <div class="form-group">
                            <label class="form-label">Country <span class="required">*</span></label>
                            <select name="country" class="form-input select-input" required>
                                <option value="USA">United States</option>
                            </select>
                        </div>
                    </div>
                </div>

                <!-- Payment Method Selection -->
                <div class="form-section">
                    <h3>Choose Payment Method</h3>
                    <div class="payment-buttons">
                        <button type="submit" name="payment_method" value="bitcoin" class="btn btn-primary payment-btn" <?php echo !$product || !$package_size ? 'disabled' : ''; ?>>
                            Pay with Bitcoin
                        </button>
                        <button type="submit" name="payment_method" value="other" class="btn btn-outline payment-btn" <?php echo !$product || !$package_size ? 'disabled' : ''; ?>>
                            Pay with Other
                        </button>
                    </div>
                    <?php if (!$product || !$package_size): ?>
                        <p style="text-align: center; color: var(--gray-500); margin-top: 1rem; font-size: 0.9rem;">
                            Please select a product to continue
                        </p>
                    <?php endif; ?>
                </div>
            </form>
        </div>
    </section>
</body>
</html>
