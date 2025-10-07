<?php
// Get the filename of the current page to dynamically set the active navigation link.
$currentPage = basename($_SERVER['PHP_SELF']);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- These meta tags can be updated dynamically on each page if needed -->
    <title>JPeptics</title>
    <meta name="description" content="Nootropics Research Store offers high-quality research products with tested and transparent quality.">
    <link rel="canonical" href="https://jpeptics.com/<?php echo htmlspecialchars($currentPage); ?>">
    <link rel="stylesheet" href="assets/css/styles.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
        <!-- Header -->
    <header class="header">
        <div class="container">
            <nav class="nav">
                <div class="logo-container">
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

    <main>

