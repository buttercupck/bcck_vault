<?php
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JPeptics - Research Peptides</title>
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
            height: 100px;
            width: auto;
            max-width: 300px;
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

        .btn-secondary {
            background: var(--primary-magenta);
            color: var(--white);
        }

        .btn-lg {
            padding: 1rem 2rem;
            font-size: 1.125rem;
        }

        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-magenta) 100%);
            color: var(--white);
            padding: 5rem 0;
            text-align: center;
        }

        .hero h1 {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 1.5rem;
            line-height: 1.1;
        }

        .hero .lead {
            font-size: 1.75rem;
            margin-bottom: 2rem;
            max-width: 1250px;
            margin-left: auto;
            margin-right: auto;
            opacity: 0.95;
            text-align: left;
            line-height: 1.5;
        }

        .hero .lead-emphasis {
            font-size: 2rem;
            font-weight: 700;
            display: block;
            margin-top: 1.5rem;
        }

        .heading-2 {
            font-size: 2rem;
            font-weight: 700;
            text-align: center;
            margin-top: 2rem;
        }

        /* Section Styles */
        .section {
            padding: 5rem 0;
        }

        .section-title {
            font-size: 2.5rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 3rem;
            color: var(--gray-800);
        }

        /* Product Grid */
        .product-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }

        .product-card {
            background: var(--white);
            border-radius: var(--radius-xl);
            overflow: hidden;
            box-shadow: var(--shadow-md);
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .product-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
        }

        .product-image {
            height: 320px;
            background: var(--gray-100);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            padding: 1rem;
        }

        .product-image img {
            width: 100%;
            height: 100%;
            object-fit: contain;
            max-width: none;
            max-height: none;
        }

        .product-content {
            padding: 2rem;
        }

        .product-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--gray-800);
        }

        .product-description {
            color: var(--gray-600);
            margin-bottom: 1rem;
        }

        .price {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-blue);
            margin-bottom: 1rem;
        }

        /* Payment Section */
        .payment-info {
            background: var(--white);
            border-radius: var(--radius-xl);
            padding: 2rem;
            box-shadow: var(--shadow-md);
            text-align: center;
            margin: 2rem 0;
        }

        .payment-info h3 {
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--gray-800);
            margin-bottom: 1rem;
        }

        .payment-info p {
            font-size: 1rem;
            color: var(--gray-700);
            margin-bottom: 1.5rem;
        }

        .payment-logos {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 2rem;
            margin: 1.5rem 0;
        }

        .payment-logo-container {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 120px;
            height: 60px;
            background: var(--gray-50);
            border: 1px solid var(--gray-200);
            border-radius: var(--radius-lg);
            padding: 0.75rem;
            transition: all 0.2s;
        }

        .payment-logo-container:hover {
            border-color: var(--primary-blue-light);
            background: var(--primary-blue-pale);
        }

        .payment-logo-container img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }

        .payment-button {
            background: var(--primary-blue);
            color: var(--white);
            padding: 0.75rem 1.5rem;
            border-radius: var(--radius-lg);
            font-size: 0.9rem;
            font-weight: 600;
            text-decoration: none;
            display: inline-block;
            margin-top: 1rem;
            transition: all 0.2s;
        }

        .payment-button:hover {
            background: var(--primary-blue-dark);
            transform: translateY(-1px);
        }

        /* COA Section */
        .coa-info {
            background: var(--primary-blue-pale);
            border-radius: var(--radius-xl);
            padding: 2rem;
            margin: 2rem 0;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero h1 { font-size: 2.5rem; }
            .nav-links { display: none; }
            .product-grid { grid-template-columns: 1fr; }
            .product-image { 
                height: 280px; 
                padding: 0.75rem;
            }
            .payment-info { 
                padding: 1.5rem; 
            }
            .payment-logos { 
                flex-direction: column; 
                gap: 1rem; 
            }
            .payment-logo-container { 
                width: 100px; 
                height: 50px; 
            }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header class="header">
        <div class="container">
            <nav class="nav">
                <div class="logo">
                    <img src="assets/logos/jpeptics-logo.png" alt="JPeptics" class="logo">
                </div>
                <ul class="nav-links">
                    <li><a href="index.php" class="nav-link">Home</a></li>
                    <li><a href="products-page.php" class="nav-link">Products</a></li>
                    <li><a href="#" class="nav-link">Support</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <p class="lead">We believe access to research peptides shouldn't come with uncertainty or inflated prices.<br><br>Reliability matters.<br><br>That's why we carefully source only small controlled batches, independently test them here in U.S. labs, and every Certificate of Analysis is linked directly to the product you receive.<br>No guessing, no worrying - just verified, transparent quality in every vial<span class="lead-emphasis">Tested, Trusted, Transparent.</span></p>
            <a href="products-page.php" class="btn btn-secondary btn-lg">Shop Now</a>
            <h2 class="heading-2">RESEARCH ONLY - NOT FOR HUMAN CONSUMPTION!</h2>
        </div>
    </section>

    <!-- Footer -->
    <footer style="background: var(--gray-800); color: var(--white); padding: 3rem 0; text-align: center; margin-top: 4rem;">
        <div class="container">
            <img src="https://f004.backblazeb2.com/file/jpeptics/assets/logos-0925/JPEPTICS-LOGO-MAIN-TRANSPARENT.png" alt="JPeptics" style="height: 60px; margin-bottom: 1rem; opacity: 0.8;">
            <p style="margin: 0; color: var(--gray-300);">All Products Sold are for Research Purposes ONLY</p>
        </div>
    </footer>
</body>
</html>
