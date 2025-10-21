<?php
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bitcoin Payment Guide - JPeptics</title>
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
            margin-bottom: 1rem;
            color: var(--gray-800);
        }

        .section-subtitle {
            text-align: center;
            max-width: 600px;
            margin: 0 auto 3rem auto;
            font-size: 1.125rem;
            color: var(--gray-600);
        }

        /* Bitcoin Steps */
        .bitcoin-guide {
            background: var(--white);
            border-radius: var(--radius-xl);
            padding: 3rem;
            box-shadow: var(--shadow-md);
            max-width: 800px;
            margin: 0 auto;
        }

        .step {
            display: flex;
            align-items: flex-start;
            margin-bottom: 3rem;
            padding-bottom: 3rem;
            border-bottom: 1px solid var(--gray-200);
        }

        .step:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }

        .step-number {
            background: var(--primary-blue);
            color: var(--white);
            width: 3rem;
            height: 3rem;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.25rem;
            margin-right: 1.5rem;
            flex-shrink: 0;
        }

        .step-content h3 {
            color: var(--gray-800);
            margin-bottom: 0.75rem;
            font-size: 1.5rem;
            font-weight: 600;
        }

        .step-content p {
            color: var(--gray-600);
            margin-bottom: 1rem;
            line-height: 1.7;
        }

        .step-checklist {
            list-style: none;
            margin: 1rem 0;
        }

        .step-checklist li {
            display: flex;
            align-items: center;
            margin-bottom: 0.5rem;
            color: var(--gray-600);
        }

        .step-checklist li::before {
            content: "☐";
            color: var(--primary-blue);
            font-weight: bold;
            margin-right: 0.75rem;
            font-size: 1.1rem;
        }

        /* Payment Logos Section */
        .payment-logos-section {
            text-align: center;
            margin: 3rem 0;
        }

        .payment-logos {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin: 2rem 0;
        }

        .payment-logo {
            width: 150px;
            height: 100px;
            background: var(--gray-100);
            border-radius: var(--radius-lg);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: var(--shadow-md);
        }

        .payment-logo img {
            max-width: 100px;
            max-height: 100px;
        }

        /* Help Section */
        .help-section {
            background: var(--primary-blue-pale);
            border-radius: var(--radius-xl);
            padding: 2rem;
            margin-top: 3rem;
            border: 1px solid var(--primary-blue-light);
        }

        .help-section h3 {
            color: var(--primary-blue-dark);
            margin-bottom: 1rem;
            font-size: 1.25rem;
        }

        .help-section ul {
            margin-left: 2rem;
            color: var(--gray-600);
        }

        .help-section li {
            margin-bottom: 0.5rem;
        }

        @media (max-width: 768px) {
            .nav-links { display: none; }
            .bitcoin-guide { padding: 2rem; }
            .step { flex-direction: column; text-align: center; }
            .step-number { margin-right: 0; margin-bottom: 1rem; }
            .payment-logos { flex-direction: column; align-items: center; }
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

    <!-- Bitcoin Payment Guide Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">Bitcoin Payment Guide</h2>
            <p class="section-subtitle">Follow these simple steps to set up Bitcoin payment through CashApp - our preferred and easiest method.</p>

            <div class="bitcoin-guide">
                <!-- Step 1: Download CashApp -->
                <div class="step">
                    <div class="step-number">1</div>
                    <div class="step-content">
                        <h3>Download CashApp</h3>
                        <p>Download the CashApp mobile application from your device's app store. CashApp is available for both iOS and Android devices and is one of the most user-friendly ways to buy and send Bitcoin.</p>
                        <div style="text-align: center; margin: 1rem 0;">
                            <div class="payment-logo" style="display: inline-flex; margin: 0 1rem;">
                                <img src="https://f004.backblazeb2.com/file/jpeptics/assets/3rd-partyLogos/Square_Cash_app_logo.svg" alt="CashApp">
                            </div>
                        </div>
                        <p style="font-style: italic; color: var(--gray-500);">Available on App Store and Google Play</p>
                    </div>
                </div>

                <!-- Step 2: Set Up Bitcoin -->
                <div class="step">
                    <div class="step-number">2</div>
                    <div class="step-content">
                        <h3>Set Up Bitcoin</h3>
                        <p>Create your CashApp account and enable Bitcoin functionality by completing these steps:</p>
                        <ul class="step-checklist">
                            <li>Create account with phone number and email</li>
                            <li>Verify identity with government ID</li>
                            <li>Add payment method (debit card or bank account)</li>
                            <li>Enable Bitcoin purchases in the app</li>
                        </ul>
                        <p>You'll need to verify your identity to enable Bitcoin features, which usually takes just a few minutes.</p>
                    </div>
                </div>

                <!-- Step 3: Purchase Bitcoin -->
                <div class="step">
                    <div class="step-number">3</div>
                    <div class="step-content">
                        <h3>Purchase Bitcoin</h3>
                        <p>Buy the exact amount of Bitcoin needed for your order, plus a small extra amount to cover network fees:</p>
                        <ul class="step-checklist">
                            <li>Buy amount needed for your order</li>
                            <li>Wait for Bitcoin to be available (usually instant)</li>
                        </ul>
                        <p>You can purchase Bitcoin instantly using your linked debit card or bank account. We recommend adding $5-10 extra to cover potential network fees.</p>
                    </div>
                </div>

                <!-- Step 4: Send Payment -->
                <div class="step">
                    <div class="step-number">4</div>
                    <div class="step-content">
                        <h3>Send Payment</h3>
                        <p>Complete your order by sending Bitcoin to our wallet address:</p>
                        <ul class="step-checklist">
                            <li>Copy our Bitcoin address (provided at checkout)</li>
                            <li>Send exact amount specified</li>
                            <li>Save transaction ID for verification</li>
                        </ul>
                        <p>After sending, CashApp will provide a transaction ID (hash). Copy this ID and submit it through our verification form to confirm your payment.</p>
                    </div>
                </div>
            </div>

            <!-- Payment Logos -->
            <div class="payment-logos-section">
                <div class="payment-logos">
                    <div class="payment-logo">
                        <img src="https://f004.backblazeb2.com/file/jpeptics/assets/3rd-partyLogos/Bitcoin.svg" alt="Bitcoin">
                    </div>
                    <div class="payment-logo">
                        <img src="https://f004.backblazeb2.com/file/jpeptics/assets/3rd-partyLogos/Square_Cash_app_logo.svg" alt="CashApp">
                    </div>
                </div>
                <p style="margin: 1rem 0; color: var(--gray-600);">Ready to complete your payment?</p>
                <a href="btc-trans-verification.php" class="btn btn-primary btn-lg">Continue to Checkout</a>
            </div>

            <!-- Help Section -->
            <div class="help-section">
                <h3>Need Help?</h3>
                <p style="margin-bottom: 1rem; color: var(--gray-600);">If you need assistance with any step:</p>
                <ul>
                    <li>Contact support at JPeptics@gmail.com</li>
                    <li>Include your order information and the step you're having trouble with</li>
                    <li>We typically respond within 1-2 hours during business hours</li>
                </ul>
            </div>
        </div>
    </section>
</body>
</html>