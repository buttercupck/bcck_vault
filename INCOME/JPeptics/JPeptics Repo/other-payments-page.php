<?php
session_start();

// Get order data from session or redirect if no order
if (!isset($_SESSION['order_data'])) {
    header('Location: order-form.php');
    exit;
}

$order_data = $_SESSION['order_data'];
$product = $order_data['product'];
$package_size = $order_data['package_size'];
$quantity = $order_data['quantity'];
$price = (float)$order_data['price'];
$shipping = 5.00; // $5 shipping charge
$total = $price + $shipping;

// Parse package information
$package_parts = explode('-', $package_size);
$pack_count = $package_parts[0] ?? '';

// Product display names
$product_names = [
    'tirzepatide' => 'Tirzepatide',
    'retatrutide' => 'Retatrutide'
];
$product_display = $product_names[$product] ?? '';
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Other Payment Options - JPeptics</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,300;1,400;1,500;1,700&family=Source+Sans+Pro:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600&display=swap');
        
        :root {
            --primary-blue: #428ce0;
            --primary-blue-dark: #3574c4;
            --primary-blue-light: #5fa3e8;
            --primary-blue-pale: #e8f2fd;
            --primary-magenta: #e11e6e;
            --primary-magenta-dark: #c71958;
            --primary-magenta-light: #e85bb6;
            --primary-magenta-pale: #fdeaf7;
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
            font-size: 1.75rem;
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
            margin-top: 0.5rem;
        }

        /* Confirmation Alert */
        .confirmation-alert {
            background: var(--success);
            color: var(--white);
            border-radius: var(--radius-xl);
            padding: 3rem;
            text-align: center;
            margin-bottom: 2rem;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            box-shadow: var(--shadow-lg);
        }

        .confirmation-alert h2 {
            font-size: 2rem;
            margin-bottom: 1rem;
        }

        .confirmation-alert p {
            font-size: 1.1rem;
            line-height: 1.7;
            margin-bottom: 1rem;
        }

        .order-number {
            background: rgba(255, 255, 255, 0.2);
            border-radius: var(--radius-lg);
            padding: 1rem;
            margin: 1.5rem 0;
            font-weight: 600;
            font-size: 1.2rem;
        }

        /* Contact Info */
        .contact-info {
            background: var(--primary-blue-pale);
            border-radius: var(--radius-xl);
            padding: 3rem;
            margin-top: 2rem;
            text-align: center;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
        }

        .contact-info h3 {
            color: var(--primary-blue-dark);
            margin-bottom: 1rem;
        }

        .contact-info p {
            color: var(--gray-600);
            font-size: 1.1rem;
        }

        @media (max-width: 768px) {
            .nav-links { display: none; }
            .order-summary { 
                margin: 0 1rem 2rem 1rem; 
                padding: 2rem;
            }
            .confirmation-alert { 
                margin: 0 1rem 2rem 1rem; 
                padding: 2rem;
            }
            .contact-info { 
                margin: 2rem 1rem 0 1rem; 
                padding: 2rem;
            }
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

    <!-- Order Confirmation Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">Order Confirmation</h2>
            
            <!-- Confirmation Alert -->
            <div class="confirmation-alert">
                <h2>Order Received!</h2>
                <p>Thank you for your order. We have received your request and will contact you shortly with payment options.</p>
                <div class="order-number">
                    Order #<?php echo htmlspecialchars($order_data['order_number']); ?>
                </div>
                <p>Please save this order number for your records.</p>
            </div>

            <!-- Order Summary -->
            <div class="order-summary <?php echo $product; ?>">
                <h3>Order Summary</h3>
                <div class="order-item">
                    <span><?php echo $quantity; ?>x <?php echo $product_display; ?> <?php echo $pack_count; ?> pack</span>
                    <span>$<?php echo number_format($price, 2); ?></span>
                </div>
                <div class="order-item">
                    <span>Shipping</span>
                    <span>$<?php echo number_format($shipping, 2); ?></span>
                </div>
                <div class="order-item">
                    <span><strong>Total</strong></span>
                    <span><strong>$<?php echo number_format($total, 2); ?></strong></span>
                </div>
            </div>

            <!-- Contact Information -->
            <div class="contact-info">
                <h3>What Happens Next?</h3>
                <p>Our team will contact you within 24 hours at <strong><?php echo htmlspecialchars($order_data['customer_info']['email']); ?></strong> with available payment options and instructions to complete your order.</p>
                <p style="margin-top: 1rem;">If you have any questions, please contact us at <strong>JPeptics@gmail.com</strong></p>
            </div>
        </div>
    </section>
</body>
</html>