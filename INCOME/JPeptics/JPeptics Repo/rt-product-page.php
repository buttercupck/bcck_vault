<?php
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Retatrutide - JPeptics Research Peptides</title>
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

        .btn-outline {
            background: transparent;
            color: var(--primary-blue);
            border: 2px solid var(--primary-blue);
        }

        .btn-lg {
            padding: 1rem 2rem;
            font-size: 1.125rem;
        }

        /* Section Styles */
        .section {
            padding: 3rem 0;
        }

        /* Product Detail Grid */
        .product-detail {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            align-items: start;
            margin-bottom: 4rem;
        }

        .product-images {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .main-image-container {
            width: 100%;
            max-width: 400px;
            height: 400px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow-lg);
            background: var(--white);
        }

        .main-image {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }

        .product-info h1 {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--primary-blue);
            margin-bottom: 1rem;
        }

        .product-description {
            font-size: 1.125rem;
            color: var(--gray-600);
            margin-bottom: 2rem;
            line-height: 1.7;
        }

        /* Form Styles with Blue Theming */
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
            border: 2px solid var(--primary-blue-light);
            border-radius: var(--radius-lg);
            font-size: 1rem;
            transition: border-color 0.2s;
            font-family: var(--font-primary);
        }

        .form-input:focus {
            outline: none;
            border-color: var(--primary-blue);
            box-shadow: 0 0 0 3px rgba(66, 140, 224, 0.1);
        }

        .select-input {
            background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%2342%8ce0' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
            background-position: right 0.75rem center;
            background-repeat: no-repeat;
            background-size: 1.5em 1.5em;
            padding-right: 2.5rem;
            appearance: none;
        }

        /* Bitcoin Bonus Section */
        .whats-included {
            background: var(--gray-50);
            border-radius: var(--radius-xl);
            padding: 3rem;
            margin: 4rem 0;
            border: 1px solid var(--gray-200);
            border-left: 4px solid var(--primary-blue);
        }

        .bonus-content {
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 2rem;
            align-items: start;
        }

        .bonus-image {
            width: 450px;
            height: 400px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--white);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
            padding: 1rem;
        }

        .bonus-image img {
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }

        .bonus-text-section {
            display: flex;
            flex-direction: column;
        }

        .bonus-text-section h3 {
            font-size: 1.75rem;
            font-weight: 600;
            color: var(--primary-blue);
            margin-bottom: 1.5rem;
            margin-top: 0;
        }

        .bonus-list {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .bonus-item {
            display: flex;
            align-items: center;
            font-size: 1.1rem;
            font-weight: 500;
            color: var(--gray-700);
        }

        .bonus-item::before {
            content: "✓";
            color: var(--primary-blue);
            font-weight: bold;
            margin-right: 0.75rem;
            font-size: 1.25rem;
        }

        .total-savings {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--primary-blue);
            margin-top: 0.5rem;
        }

        /* COA Section with Blue Theming */
        .coa-section {
            background: rgba(66, 140, 224, 0.1);
            border-radius: var(--radius-xl);
            padding: 3rem;
            margin: 4rem 0;
            border: 2px solid var(--primary-blue-light);
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 2rem;
            align-items: center;
        }

        .coa-content h3 {
            font-size: 2rem;
            font-weight: 600;
            color: var(--primary-blue-dark);
            margin-bottom: 1rem;
        }

        .coa-content ul {
            margin: 1rem 0 2rem 2rem;
            color: var(--gray-600);
        }

        .coa-content li {
            margin-bottom: 0.5rem;
        }

        .coa-image img {
            max-width: 200px;
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
        }

        @media (max-width: 768px) {
            .nav-links { display: none; }
            .product-detail { grid-template-columns: 1fr; gap: 2rem; }
            .included-grid { grid-template-columns: 1fr; }
            .whats-included { padding: 2rem; }
            .coa-section { padding: 2rem; }
        }
    </style>
</head>
<body>
    <!-- Header -->
 <?php include 'partials/header.php'; ?>

    <!-- Product Detail Section -->
    <section class="section">
        <div class="container">
            <div class="product-detail">
                <div class="product-images">
                    <div class="main-image-container">
                        <img id="mainImage" src="https://f004.backblazeb2.com/file/jpeptics/assets/RT-0925/RT-SINGLE-LABEL-A-JP-RITA-0925.png.png" alt="Retatrutide" class="main-image">
                    </div>
                </div>
                <div class="product-info">
                    <h1>Retatrutide</h1>
                    <p class="product-description">Retatrutide is a research peptide that activates three different hormone receptors at once—GLP-1, GIP, and glucagon—to give scientists a way to study how these systems work together. Its triple action is being investigated for potential roles in weight management, blood sugar regulation, and metabolism.</p>
                    
                    <form method="POST" action="order-form.php">
                        <input type="hidden" name="product" value="retatrutide">
                        
                        <div class="form-group">
                            <label class="form-label">Package Size</label>
                            <select name="package_size" class="form-input select-input" required onchange="updateGallery(this.value)">
                                <option value="">Select package size</option>
                                <option value="3-pack-179">3 pack - $179</option>
                                <option value="6-pack-339">6 pack - $339</option>
                                <option value="10-pack-529">10 pack - $529</option>
                            </select>
                        </div>
                        
                        <div class="form-group">
                            <label class="form-label">Quantity</label>
                            <select name="quantity" class="form-input select-input" required>
                                <option value="1">1</option>
                            </select>
                            <small style="color: var(--gray-600); margin-top: 0.5rem; display: block;">Maximum 1 quantity per order</small>
                        </div>
                        
                        <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;">Add to Cart - Proceed to Payment</button>
                    </form>
                </div>
            </div>

           
            <!-- COA Information -->
            <div class="coa-section">
                <div class="coa-content">
                    <h3>Certificate of Analysis</h3>
                    <p style="color: var(--gray-600); margin-bottom: 1rem;">Each batch of Tirzepatide comes with a complete Certificate of Analysis showing:</p>
                    <ul>
                       <li>Purity testing results</li>
                        <li>Identity verification</li>
                        <li>Potency analysis</li>
                        <li>Contaminant screening</li>
                        <li>Batch-specific data</li>
                        <li>Purity testing results</li>
                        <li>Identity verification</li>
                        <li>Potency analysis</li>
                        <li>Batch number</li> 
                        <li>-Unique cap color</li>
                        <li>Exact batch size</li>
                    </ul>
                    <a href="coa-page.php" class="btn btn-outline">View Current COA</a>
                </div>
                <div class="coa-image">
                    <img src="assets/products/RZ/RT-3PK-PACK-A-JP-RITA-0925.svg" alt="JPeptics" alt="3-PK-RT">
                </div>
            </div>
        </div>
    </section>
// <---Footer--->
        <?php include 'partials/footer.php'; ?>
    <script>
        // Image URLs for different package sizes
        const packageImages = {
            '3-pack-179': {
                url: 'https://f004.backblazeb2.com/file/jpeptics/assets/RT-0925/RT-3PK-PACK-A-JP-RITA-0925.png.png',
                alt: '3 Pack Retatrutide'
            },
            '6-pack-339': {
                url: 'https://f004.backblazeb2.com/file/jpeptics/assets/RT-0925/RT-6PK-PACK-A-JP-RITA-0925.png.png',
                alt: '6 Pack Retatrutide'
            },
            '10-pack-529': {
                url: 'https://f004.backblazeb2.com/file/jpeptics/assets/RT-0925/RT-10PK-PACK-A-JP-RITA-0925.png.png',
                alt: '10 Pack Retatrutide'
            }
        };

        const labelImage = {
            url: 'https://f004.backblazeb2.com/file/jpeptics/assets/RT-0925/RT-SINGLE-LABEL-A-JP-RITA-0925.png.png',
            alt: 'Retatrutide Label'
        };

        function updateGallery(packageSize) {
            const mainImage = document.getElementById('mainImage');
            
            if (!packageSize) {
                // Reset to label image
                mainImage.src = labelImage.url;
                mainImage.alt = labelImage.alt;
                return;
            }

            const selectedPackage = packageImages[packageSize];
            
            if (selectedPackage) {
                // Update main image to package image
                mainImage.src = selectedPackage.url;
                mainImage.alt = selectedPackage.alt;
            }
        }
    </script>
</body>
</html>
