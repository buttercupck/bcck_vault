<?php
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Products - JPeptics Research Peptides</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,300;1,400;1,500;1,700&family=Source+Sans+Pro:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600&display=swap');
        
        :root {
            --primary-blue: #428ce0;
            --primary-blue-dark: #3574c4;
            --primary-blue-light: #5fa3e8;
            --primary-blue-pale: #e8f2fd;
            --primary-magenta: #e344aa;
            --primary-magenta-dark: #cc3d9a;
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

        .btn-outline {
            background: transparent;
            color: var(--primary-blue);
            border: 2px solid var(--primary-blue);
        }

        .btn-outline:hover {
            background: var(--primary-blue);
            color: var(--white);
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

        /* Product Grid */
        .product-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin-bottom: 4rem;
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
            height: 280px;
            background: var(--gray-100);
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }

        .product-image img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
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
            margin-bottom: 1.5rem;
            line-height: 1.6;
        }

        .price {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-blue);
            margin-bottom: 1rem;
        }

        /* Tirzepatide Theming */
        .product-card.tirzepatide .product-title {
            color: var(--primary-magenta);
        }

        .product-card.tirzepatide .price {
            color: var(--primary-magenta);
        }

        .product-card.tirzepatide .btn-outline {
            color: var(--primary-magenta);
            border-color: var(--primary-magenta);
        }

        .product-card.tirzepatide .btn-outline:hover {
            background: var(--primary-magenta);
            color: var(--white);
        }

        .product-card.tirzepatide .btn-primary {
            background: var(--primary-magenta);
        }

        /* Retatrutide Theming */
        .product-card.retatrutide .product-title {
            color: var(--primary-blue);
        }

        .product-card.retatrutide .price {
            color: var(--primary-blue);
        }

        .product-card.retatrutide .btn-outline {
            color: var(--primary-blue);
            border-color: var(--primary-blue);
        }

        .product-card.retatrutide .btn-outline:hover {
            background: var(--primary-blue);
            color: var(--white);
        }

        .product-card.retatrutide .btn-primary {
            background: var(--primary-blue);
        }

        .product-card.retatrutide .btn-primary:hover {
            background: var(--primary-blue-dark);
        }

        /* COA Section */
        .coa-section {
            background: linear-gradient(135deg, var(--primary-magenta) 0%, var(--primary-blue) 100%);
            border-radius: var(--radius-xl);
            padding: 3rem;
            margin: 4rem 0;
            border: 1px solid var(--primary-magenta-light);
            color: var(--white);
        }

        .coa-section h3 {
            font-size: 2rem;
            font-weight: 600;
            color: var(--white);
            margin-bottom: 1rem;
            text-align: center;
        }

        .coa-description {
            text-align: center;
            color: var(--white);
            margin-bottom: 2rem;
            font-size: 1.1rem;
            opacity: 0.95;
        }

        .coa-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
        }

        .coa-btn {
            background: rgba(255, 255, 255, 0.2);
            color: var(--white);
            border: 2px solid rgba(255, 255, 255, 0.3);
            padding: 0.75rem 1.5rem;
            border-radius: var(--radius-lg);
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
            display: inline-block;
            text-align: center;
        }

        .coa-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            border-color: rgba(255, 255, 255, 0.5);
            transform: translateY(-2px);
        }

        .coa-btn.tz:hover {
            background: var(--primary-magenta);
            border-color: var(--primary-magenta);
        }

        .coa-btn.rz:hover {
            background: var(--primary-blue);
            border-color: var(--primary-blue);
        }

        @media (max-width: 768px) {
            .nav-links { display: none; }
            .product-grid { grid-template-columns: 1fr; }
            .coa-grid { grid-template-columns: 1fr; }
            .coa-section { padding: 2rem; }
        }
    </style>
</head>
<body>
    <!-- Header -->
   <?php include 'partials/header.php'; ?>

    <!-- Products Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">Research Peptides</h2>

            <div style="max-width: 900px; margin: 0 auto 3rem auto; text-align: center;">
                <p style="font-size: 1.125rem; line-height: 1.8; color: var(--gray-700);">
                    At JPeptics, we don't carry dozens of products, we keep it simple. We concentrate on the two most in-demand GLP-1 peptides on the market, Tirzepatide and Retatrutide. Why?<br>
                    It allows us to focus on unmatched quality control, independent U.S. testing, and full transparency—so you know exactly what you're getting.<br>
                    <strong>Tested. Trusted. Transparent.</strong>
                </p>
            </div>

            <div class="product-grid">
                <!-- Tirzepatide Product Card -->
                <div class="product-card tirzepatide">
                    <div class="product-image">
                        <img src="https://f004.backblazeb2.com/file/jpeptics/assets/TZ-0925/TZ-Vile.jpeg" alt="Tirzepatide">
                    </div>
                    <div class="product-content">
                        <h3 class="product-title">Tirzepatide 30mg</h3>
                        <p class="product-description">A lab-made compound that can interact with two natural receptors in the body at the same time. By activating both, it helps researchers study how these pathways may work together in regulating metabolism and blood sugar.</p>
                        <div style="display: flex; gap: 1.5rem; margin-top: 1.5rem;">
                            <a href="tz-product-page.php" class="btn btn-outline" style="flex: 1;">View Details</a>
                        </div>
                        <p style="text-align: center; font-size: 1.5rem; color: #EF4444; font-weight: 600; padding-top: 1rem; margin-top: 1rem; border-top: 1px solid var(--gray-200);">RESEARCH USE ONLY - NOT FOR HUMAN CONSUMPTION!</p>
                    </div>
                </div>
                
                <!-- Retatrutide Product Card -->
                <div class="product-card retatrutide">
                    <div class="product-image">
                        <img src="https://f004.backblazeb2.com/file/jpeptics/assets/RT-0925/RT-SINGLE-VIAL-A-JP-RITA-0925.png.png" alt="Retatrutide">
                    </div>
                    <div class="product-content">
                        <h3 class="product-title">Retatrutide 20mg</h3>
                        <p class="product-description">A research peptide that activates three different hormone receptors at once—GLP-1, GIP, and glucagon—to give scientists a way to study how these systems work together. Its triple action is being investigated for potential roles in weight management, blood sugar regulation, and metabolism.</p>
                        <div style="display: flex; gap: 1.5rem; margin-top: 1.5rem;">
                            <a href="rt-product-page.php" class="btn btn-outline" style="flex: 1;">View Details</a>
                        </div>
                        <p style="text-align: center; font-size: 1.5rem; color: #EF4444; font-weight: 600; padding-top: 1rem; margin-top: 1rem; border-top: 1px solid var(--gray-200);">RESEARCH USE ONLY - NOT FOR HUMAN CONSUMPTION!</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
<?php include 'partials/footer.php'; ?>
