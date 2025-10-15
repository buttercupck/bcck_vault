<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JPeptics - Research Peptides | Tested, Trusted, Transparent</title>
    <meta name="description" content="High-quality research peptides with independent U.S. lab testing. Tirzepatide and Retatrutide with full Certificate of Analysis.">
    
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    
    <!-- Custom Tailwind Config -->
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'tirzepatide': {
                            50: '#fdf2f8',
                            100: '#fce7f3',
                            200: '#fbcfe8',
                            300: '#f9a8d4',
                            400: '#f472b6',
                            500: '#ec4899',
                            600: '#db2777',
                            700: '#be185d',
                            800: '#9d174d',
                            900: '#831843',
                        },
                        'retatrutide': {
                            50: '#eff6ff',
                            100: '#dbeafe',
                            200: '#bfdbfe',
                            300: '#93c5fd',
                            400: '#60a5fa',
                            500: '#3b82f6',
                            600: '#2563eb',
                            700: '#1d4ed8',
                            800: '#1e40af',
                            900: '#1e3a8a',
                        }
                    }
                }
            }
        }
    </script>
    
    <!-- Custom CSS -->
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        body {
            font-family: 'Inter', sans-serif;
        }
        
        .fade-in {
            animation: fadeIn 0.6s ease-in-out;
        }
        
        .slide-up {
            animation: slideUp 0.5s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .card-hover {
            transition: all 0.3s ease;
        }
        
        .card-hover:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        
        .btn-tirzepatide {
            background: linear-gradient(135deg, #ec4899 0%, #db2777 100%);
        }
        
        .btn-retatrutide {
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        }
        
        .product-card-tirzepatide {
            border-color: #f9a8d4;
            background: linear-gradient(135deg, #fdf2f8 0%, #ffffff 100%);
        }
        
        .product-card-retatrutide {
            border-color: #93c5fd;
            background: linear-gradient(135deg, #eff6ff 0%, #ffffff 100%);
        }
    </style>
</head>
<body class="bg-gray-50 min-h-screen">

    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <!-- Logo -->
                <div class="flex items-center">
                    <a href="index.php" class="flex items-center">
                        <img src="assets/logos/jpeptics-logo.png" alt="JPeptics" class="h-8 w-auto">
                        <span class="ml-2 text-xl font-bold text-gray-900">JPeptics</span>
                    </a>
                </div>

                <!-- Navigation -->
                <nav class="hidden md:flex space-x-8">
                    <a href="index.php" class="text-gray-600 hover:text-gray-900 px-3 py-2 text-sm font-medium transition-colors">Home</a>
                    <a href="#about" class="text-gray-600 hover:text-gray-900 px-3 py-2 text-sm font-medium transition-colors">About</a>
                </nav>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        <!-- Hero Section -->
        <section class="mb-16 fade-in">
            <div class="max-w-4xl mx-auto">
                <p class="text-xl text-gray-600 mb-8 leading-relaxed text-left">
                    We believe access to research peptides shouldn't come with uncertainty or inflated prices.<br>
                    Reliability matters.<br>
                    That's why we carefully source only small controlled batches, independently test them here in U.S. labs, and every Certificate of Analysis is linked directly to the product you receive.<br>
                    No guessing, no worrying - just verified, transparent quality in every vial.<br>
                    Tested, Trusted, Transparent.
                </p>
            </div>
        </section>

        <!-- Products Section -->
        <section id="products" class="mb-16 slide-up">

            <div class="grid md:grid-cols-2 gap-8 max-w-5xl mx-auto">
                <!-- Tirzepatide Product Card -->
                <div class="product-card-tirzepatide border-2 rounded-xl p-8 card-hover">
                    <div class="text-center mb-6">
                        <div class="w-24 h-24 mx-auto mb-4 bg-white rounded-full flex items-center justify-center shadow-lg">
                            <div class="w-16 h-16 bg-tirzepatide-100 rounded-full flex items-center justify-center">
                                <span class="text-tirzepatide-600 font-bold text-lg">TZ</span>
                            </div>
                        </div>
                        <h3 class="text-2xl font-bold text-gray-900">Tirzepatide 30mg</h3>
                        <p class="text-tirzepatide-600 font-semibold text-lg">Below $2/mg!</p>
                    </div>

                    <div class="mb-6">
                        <p class="text-gray-700 text-center">
                            At JPeptics, we don't carry dozens of products, we keep it simple. We concentrate on the two most in-demand GLP-1 peptides on the market, Tirzepatide and Retatrutide. Why?  It allows us to focus on unmatched quality control, independent U.S. testing, and full transparency-so you know exactly what you're getting.<br>
                            Tested. Trusted. Transparent.
                        </p>
                    </div>

                    <div class="space-y-4">
                        <div class="grid grid-cols-2 gap-3">
                            <a href="products-page.php" class="bg-gray-100 hover:bg-gray-200 text-gray-900 px-4 py-3 rounded-lg font-semibold transition-colors text-center">
                                View Details
                            </a>
                            <a href="coa-page.php" class="bg-tirzepatide-100 hover:bg-tirzepatide-200 text-tirzepatide-700 px-4 py-3 rounded-lg font-semibold transition-colors text-center">
                                View COA's
                            </a>
                        </div>

                        <div class="text-center pt-4 border-t border-gray-200">
                            <p class="text-xs text-red-600 font-semibold">RESEARCH USE ONLY - NOT FOR HUMAN CONSUMPTION!</p>
                        </div>
                    </div>
                </div>

                <!-- Retatrutide Product Card -->
                <div class="product-card-retatrutide border-2 rounded-xl p-8 card-hover">
                    <div class="text-center mb-6">
                        <div class="w-24 h-24 mx-auto mb-4 bg-white rounded-full flex items-center justify-center shadow-lg">
                            <div class="w-16 h-16 bg-retatrutide-100 rounded-full flex items-center justify-center">
                                <span class="text-retatrutide-600 font-bold text-lg">RT</span>
                            </div>
                        </div>
                        <h3 class="text-2xl font-bold text-gray-900">Retatrutide</h3>
                        <p class="text-retatrutide-600 font-semibold">20mg • GLP-1/GIP/Glucagon Triple Agonist</p>
                        <p class="text-sm text-gray-600 mt-2">Lot JP-RITA-0925</p>
                    </div>
                    
                    <div class="mb-6">
                        <p class="text-gray-700 text-center">
                            A research peptide that activates three different hormone receptors at once—GLP-1, GIP, and glucagon—to 
                            study how these systems work together in metabolism regulation.
                        </p>
                    </div>

                    <div class="space-y-4">
                        <div class="grid grid-cols-3 gap-2 text-sm">
                            <div class="text-center">
                                <div class="font-bold text-gray-900">3-Pack</div>
                                <div class="text-retatrutide-600">$179</div>
                            </div>
                            <div class="text-center">
                                <div class="font-bold text-gray-900">6-Pack</div>
                                <div class="text-retatrutide-600">$339</div>
                            </div>
                            <div class="text-center">
                                <div class="font-bold text-gray-900">10-Pack</div>
                                <div class="text-retatrutide-600">$529</div>
                            </div>
                        </div>
                        
                        <a href="order.php?product=retatrutide" class="btn-retatrutide text-white px-6 py-3 rounded-lg font-semibold hover:opacity-90 transition-opacity w-full text-center block">
                            Order Retatrutide
                        </a>
                    </div>
                </div>
            </div>

        </section>

        <!-- Payment Information Section -->
        <section class="mb-16 slide-up">
            <div class="text-center mb-8">
                <h2 class="text-3xl font-bold text-gray-900 mb-4">PAYMENT INFORMATION</h2>
            </div>

            <div class="max-w-md mx-auto bg-white rounded-xl shadow-lg p-8 text-center">
                <p class="text-gray-600 mb-6">
                    We accept Bitcoin only as the form of payment.
                </p>

                <div class="flex items-center justify-center space-x-6 mb-6">
                    <div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center">
                        <span class="text-orange-600 font-bold text-2xl">₿</span>
                    </div>
                </div>

                <p class="text-sm text-gray-500 mb-4">
                    Bitcoin payment instructions will be provided after you place your order.
                </p>
            </div>
        </section>

        <!-- COA Section -->
        <section id="about" class="mb-16 slide-up">
            <div class="text-center mb-8">
                <h2 class="text-3xl font-bold text-gray-900 mb-4">Certificates of Analysis (COAs)</h2>
            </div>

            <div class="max-w-4xl mx-auto bg-white rounded-xl shadow-lg p-8">
                <div class="text-center mb-8">
                    <p class="text-gray-600 text-lg leading-relaxed">
                        COAs are independent lab reports that verify the identity, purity, and quality of each batch we supply.
                        We publish them so researchers can see the exact testing data tied to their product's lot number.
                        This level of transparency ensures trust, consistency, and confidence in every vial.
                    </p>
                </div>

                <div class="grid md:grid-cols-2 gap-6">
                    <div class="bg-gradient-to-br from-tirzepatide-50 to-white border border-tirzepatide-200 rounded-lg p-6">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="font-semibold text-gray-900">Tirzepatide COA</h3>
                            <span class="text-sm text-tirzepatide-600 font-medium">Lot JP-TIRZ-0925</span>
                        </div>
                        <p class="text-sm text-gray-600 mb-4">Independent lab verification for current Tirzepatide batch</p>
                        <div class="text-center py-4 border-2 border-dashed border-tirzepatide-200 rounded-lg">
                            <p class="text-sm text-gray-500">COA available with product</p>
                        </div>
                    </div>

                    <div class="bg-gradient-to-br from-retatrutide-50 to-white border border-retatrutide-200 rounded-lg p-6">
                        <div class="flex items-center justify-between mb-4">
                            <h3 class="font-semibold text-gray-900">Retatrutide COA</h3>
                            <span class="text-sm text-retatrutide-600 font-medium">Lot JP-RITA-0925</span>
                        </div>
                        <p class="text-sm text-gray-600 mb-4">Independent lab verification for current Retatrutide batch</p>
                        <div class="text-center py-4 border-2 border-dashed border-retatrutide-200 rounded-lg">
                            <p class="text-sm text-gray-500">COA available with product</p>
                        </div>
                    </div>
                </div>

                <div class="text-center mt-8">
                    <a href="coa-page.php" class="inline-block bg-gradient-to-r from-tirzepatide-500 to-retatrutide-500 text-white px-8 py-3 rounded-lg font-semibold hover:opacity-90 transition-opacity">
                        View All COAs
                    </a>
                </div>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 mt-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
            <div class="grid md:grid-cols-3 gap-8">
                <div>
                    <div class="flex items-center mb-4">
                        <img src="assets/logos/jpeptics-logo.png" alt="JPeptics" class="h-6 w-auto">
                        <span class="ml-2 text-lg font-bold text-gray-900">JPeptics</span>
                    </div>
                    <p class="text-gray-600 text-sm">
                        High-quality research peptides with independent U.S. lab testing and full transparency.
                    </p>
                </div>
                
                <div>
                    <h3 class="font-semibold text-gray-900 mb-4">Contact</h3>
                    <div class="space-y-2 text-sm text-gray-600">
                        <p>PO Box 245</p>
                        <p>Seattle, WA 98107</p>
                    </div>
                </div>
                
                <div>
                    <h3 class="font-semibold text-gray-900 mb-4">Important Notice</h3>
                    <p class="text-xs text-gray-500">
                        Disclaimer: All products are provided strictly for laboratory research purposes only. 
                        They are not intended for human or veterinary consumption.
                    </p>
                </div>
            </div>
            
            <div class="border-t border-gray-200 mt-8 pt-8 text-center">
                <p class="text-sm text-gray-500">
                    © 2024 JPeptics. All rights reserved. | Tested, Trusted, Transparent.
                </p>
            </div>
        </div>
    </footer>

</body>
</html>