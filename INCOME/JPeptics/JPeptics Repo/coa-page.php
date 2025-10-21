<?php
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Certificates of Analysis - JPeptics</title>
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

        /* Section Styles */
        .section {
            padding: 4rem 0;
        }

        .section-title {
            font-size: 2.5rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 3rem;
            color: var(--gray-800);
        }

        /* COA Grid */
        .coa-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }

        .coa-column {
            background: var(--white);
            border-radius: var(--radius-xl);
            overflow: hidden;
            box-shadow: var(--shadow-lg);
            padding: 2rem;
        }

        .coa-column.retatrutide {
            border-top: 4px solid var(--primary-blue);
        }

        .coa-column.tirzepatide {
            border-top: 4px solid var(--primary-magenta);
        }

        .coa-image {
            width: 100%;
            height: auto;
            margin-bottom: 1.5rem;
            border-radius: var(--radius-lg);
        }

        .coa-title {
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--gray-800);
        }

        .coa-column.retatrutide .coa-title {
            color: var(--primary-blue);
        }

        .coa-column.tirzepatide .coa-title {
            color: var(--primary-magenta);
        }

        .coa-body {
            margin-bottom: 1.5rem;
            color: var(--gray-700);
            line-height: 1.8;
        }

        .coa-body ul {
            margin-left: 1.5rem;
            margin-top: 0.5rem;
        }

        .coa-body li {
            margin-bottom: 0.5rem;
        }

        .btn {
            display: inline-block;
            padding: 0.875rem 1.75rem;
            border-radius: var(--radius-lg);
            font-weight: 600;
            text-decoration: none;
            cursor: pointer;
            border: none;
            transition: all 0.2s;
            text-align: center;
            width: 100%;
        }

        .button-gradient {
            background: linear-gradient(135deg, var(--primary-magenta) 0%, var(--primary-blue) 100%);
            color: var(--white);
        }

        .button-gradient:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }

        .button-primary {
            background: var(--primary-blue);
            color: var(--white);
        }

        .button-primary:hover {
            background: var(--primary-blue-dark);
            transform: translateY(-2px);
        }

        .button-lg {
            padding: 1rem 2rem;
            font-size: 1.125rem;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .nav-links { display: none; }
            .coa-grid {
                grid-template-columns: 1fr;
                gap: 2rem;
            }
            .section-title {
                font-size: 2rem;
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
                    <img src="https://f004.backblazeb2.com/file/jpeptics/assets/logos-0925/Gemini_Generated_Image_4jfbv54jfbv54jfb.png" alt="JPeptics" class="logo">
                </div>
                <ul class="nav-links">
                    <li><a href="index.php" class="nav-link">Home</a></li>
                    <li><a href="products-page.php" class="nav-link">Products</a></li>
                    <li><a href="coa-page.php" class="nav-link">COAs</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- COA Section -->
    <section class="section">
        <div class="container">
            <h2 class="section-title">Certificates of Analysis</h2>

            <div class="coa-grid">
                <!-- Retatrutide Column -->
                <div class="coa-column retatrutide">
                    <img src="https://f004.backblazeb2.com/file/jpeptics/assets/RT-0925/RT-COA-Label-JP-RITA-0925.png" alt="Retatrutide COA" class="coa-image">

                    <h3 class="coa-title">Retatrutide</h3>
                    <a href="https://f004.backblazeb2.com/file/jpeptics/COAs/sampleCOAs.jpg" target="_blank" class="btn button-gradient button-lg">
                        Retatrutide - Batch RT001
                    </a>
                </div>

                <!-- Tirzepatide Column -->
                <div class="coa-column tirzepatide">
                    <img src="https://f004.backblazeb2.com/file/jpeptics/assets/TZ-0925/TZ-COA-Label-JP-TIRZ-0925.png.png" alt="Tirzepatide COA" class="coa-image">

                    <h3 class="coa-title">Tirzepatide</h3>

                    <a href="https://f004.backblazeb2.com/file/jpeptics/assets/TZ-0925/TZ-COA-Label-JP-TIRZ-0925.png.png" target="_blank" class="btn button-primary button-lg">
                        Tirzepatide - Batch TZ001
                    </a>
                </div>
            </div>
        </div>
    </section>

    // <-- Footer -->
        <?php include 'partials/footer.php'; ?>
</body>
</html>
