```
```<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>JPeptics Design System</title>
    <style>
        /* Typography - Professional Medical/Scientific Industry Inspired */
        @import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;0,900;1,300;1,400;1,500;1,700&family=Source+Sans+Pro:ital,wght@0,300;0,400;0,600;0,700;1,300;1,400;1,600&display=swap');
        
        :root {
            /* Primary Color Palette - JPeptics Brand Colors */
            --primary-blue: #428ce0;        /* Main brand blue - trust & cognitive enhancement */
            --primary-blue-dark: #3574c4;   /* Darker blue for hover states */
            --primary-blue-light: #5fa3e8;  /* Lighter blue for backgrounds */
            --primary-blue-pale: #e8f2fd;   /* Very light blue for backgrounds */
            
            --primary-magenta: #f433a7;     /* Brand magenta - energy & vitality */
            --primary-magenta-dark: #cc3d9a; /* Darker magenta for hover states */
            --primary-magenta-light: #e85bb6; /* Lighter magenta for accents */
            --primary-magenta-pale: #fdeaf7; /* Very light magenta for backgrounds */
            
            /* Secondary Colors - Health & Wellness Theme */
            --secondary-green: #10B981;     /* Success/health green */
            --secondary-purple: #8B5CF6;    /* Premium purple for highlights */
            --secondary-orange: #F59E0B;    /* Energy/vitamin orange */
            --secondary-teal: #06B6D4;      /* Refreshing teal accent */
            
            /* System Colors - UX/UI States */
            --success: #22C55E;       /* Success actions - order confirmed */
            --warning: #F59E0B;       /* Warning states - stock low */
            --danger: #EF4444;        /* Error states - out of stock */
            --info: #3B82F6;          /* Information - product details */
            
            /* Neutral Scale - Clean & Professional */
            --white: #FFFFFF;
            --gray-50: #FAFAFA;
            --gray-100: #F5F5F5;
            --gray-200: #E5E5E5;
            --gray-300: #D4D4D4;
            --gray-400: #A3A3A3;
            --gray-500: #737373;
            --gray-600: #525252;
            --gray-700: #404040;
            --gray-800: #262626;
            --gray-900: #171717;
            
            /* Typography System */
            --font-primary: 'Roboto', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            --font-secondary: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            
            /* Font Sizes - Modular Scale 1.2x */
            --text-xs: 0.75rem;       /* 12px */
            --text-sm: 0.875rem;      /* 14px */
            --text-base: 1rem;        /* 16px */
            --text-lg: 1.125rem;      /* 18px */
            --text-xl: 1.25rem;       /* 20px */
            --text-2xl: 1.5rem;       /* 24px */
            --text-3xl: 1.875rem;     /* 30px */
            --text-4xl: 2.25rem;      /* 36px */
            --text-5xl: 3rem;         /* 48px */
            
            /* Spacing System - 8px grid */
            --space-1: 0.25rem;   /* 4px */
            --space-2: 0.5rem;    /* 8px */
            --space-3: 0.75rem;   /* 12px */
            --space-4: 1rem;      /* 16px */
            --space-5: 1.25rem;   /* 20px */
            --space-6: 1.5rem;    /* 24px */
            --space-8: 2rem;      /* 32px */
            --space-10: 2.5rem;   /* 40px */
            --space-12: 3rem;     /* 48px */
            --space-16: 4rem;     /* 64px */
            --space-20: 5rem;     /* 80px */
            
            /* Border Radius - Rounded & Friendly */
            --radius-sm: 0.25rem;   /* 4px */
            --radius-md: 0.5rem;    /* 8px */
            --radius-lg: 0.75rem;   /* 12px */
            --radius-xl: 1rem;      /* 16px */
            --radius-2xl: 1.5rem;   /* 24px */
            --radius-full: 9999px;  /* Full rounded */
            
            /* Shadows - Subtle & Modern */
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            
            /* Gradients - Modern & Energetic */
            --gradient-primary: linear-gradient(135deg, var(--primary-blue) 0%, var(--primary-magenta) 100%);
            --gradient-secondary: linear-gradient(135deg, var(--secondary-purple) 0%, var(--secondary-teal) 100%);
            --gradient-wellness: linear-gradient(135deg, var(--secondary-green) 0%, var(--secondary-teal) 100%);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: var(--font-primary);
            font-size: var(--text-base);
            line-height: 1.6;
            color: var(--gray-700);
            background-color: var(--gray-50);
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: var(--space-6);
        }
        
        /* Typography Components */
        .heading-1 {
            font-family: var(--font-primary);
            font-size: var(--text-5xl);
            font-weight: 800;
            color: var(--gray-900);
            margin-bottom: var(--space-6);
            line-height: 1.1;
        }
        
        .heading-2 {
            font-family: var(--font-primary);
            font-size: var(--text-4xl);
            font-weight: 700;
            color: var(--gray-800);
            margin-bottom: var(--space-5);
            line-height: 1.2;
        }
        
        .heading-3 {
            font-family: var(--font-primary);
            font-size: var(--text-3xl);
            font-weight: 600;
            color: var(--gray-800);
            margin-bottom: var(--space-4);
            line-height: 1.3;
        }
        
        .heading-4 {
            font-size: var(--text-2xl);
            font-weight: 600;
            color: var(--gray-700);
            margin-bottom: var(--space-3);
            line-height: 1.4;
        }
        
        .heading-5 {
            font-size: var(--text-xl);
            font-weight: 600;
            color: var(--gray-700);
            margin-bottom: var(--space-2);
            line-height: 1.4;
        }
        
        .body-large {
            font-size: var(--text-lg);
            line-height: 1.7;
            color: var(--gray-600);
        }
        
        .body-base {
            font-size: var(--text-base);
            line-height: 1.6;
            color: var(--gray-600);
        }
        
        .body-small {
            font-size: var(--text-sm);
            line-height: 1.5;
            color: var(--gray-500);
        }
        
        .caption {
            font-size: var(--text-xs);
            font-weight: 500;
            color: var(--gray-400);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .text-gradient {
            background: var(--gradient-primary);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700;
        }
        
        /* Color Palette Display */
        .color-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: var(--space-4);
            margin: var(--space-6) 0;
        }
        
        .color-card {
            background: var(--white);
            border-radius: var(--radius-xl);
            padding: var(--space-4);
            box-shadow: var(--shadow-md);
            border: 1px solid var(--gray-200);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .color-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        
        .color-swatch {
            width: 100%;
            height: 100px;
            border-radius: var(--radius-lg);
            margin-bottom: var(--space-3);
            box-shadow: var(--shadow-sm);
        }
        
        .color-name {
            font-weight: 600;
            color: var(--gray-800);
            font-size: var(--text-sm);
            margin-bottom: var(--space-1);
        }
        
        .color-value {
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: var(--text-xs);
            color: var(--gray-500);
            background: var(--gray-100);
            padding: var(--space-1) var(--space-2);
            border-radius: var(--radius-sm);
            display: inline-block;
            margin-bottom: var(--space-2);
        }
        
        .color-description {
            font-size: var(--text-xs);
            color: var(--gray-500);
            line-height: 1.4;
        }
        
        /* Button Components */
        .button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: var(--space-2);
            padding: var(--space-3) var(--space-6);
            font-size: var(--text-sm);
            font-weight: 600;
            border-radius: var(--radius-lg);
            border: none;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
            font-family: var(--font-primary);
            white-space: nowrap;
        }
        
        .button-lg {
            padding: var(--space-4) var(--space-8);
            font-size: var(--text-base);
        }
        
        .button-sm {
            padding: var(--space-2) var(--space-4);
            font-size: var(--text-xs);
        }
        
        .button-primary {
            background-color: var(--primary-blue);
            color: var(--white);
        }
        
        .button-primary:hover {
            background-color: var(--primary-blue-dark);
            transform: translateY(-1px);
            box-shadow: var(--shadow-lg);
        }
        
        .button-secondary {
            background-color: var(--primary-magenta);
            color: var(--white);
        }
        
        .button-secondary:hover {
            background-color: var(--primary-magenta-dark);
            transform: translateY(-1px);
            box-shadow: var(--shadow-lg);
        }
        
        .button-gradient {
            background: var(--gradient-primary);
            color: var(--white);
        }
        
        .button-gradient:hover {
            opacity: 0.9;
            transform: translateY(-1px);
            box-shadow: var(--shadow-lg);
        }
        
        .button-success {
            background-color: var(--success);
            color: var(--white);
        }
        
        .button-warning {
            background-color: var(--warning);
            color: var(--white);
        }
        
        .button-danger {
            background-color: var(--danger);
            color: var(--white);
        }
        
        .button-outline {
            background-color: transparent;
            color: var(--primary-blue);
            border: 2px solid var(--primary-blue);
        }
        
        .button-outline:hover {
            background-color: var(--primary-blue);
            color: var(--white);
        }
        
        .button-ghost {
            background-color: transparent;
            color: var(--gray-600);
        }
        
        .button-ghost:hover {
            background-color: var(--gray-100);
        }
        
        /* Input Components */
        .input-group {
            margin-bottom: var(--space-4);
        }
        
        .input-label {
            display: block;
            font-size: var(--text-sm);
            font-weight: 500;
            color: var(--gray-700);
            margin-bottom: var(--space-2);
        }
        
        .input {
            width: 100%;
            padding: var(--space-3);
            font-size: var(--text-base);
            border: 2px solid var(--gray-200);
            border-radius: var(--radius-lg);
            background-color: var(--white);
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
            font-family: var(--font-primary);
        }
        
        .input:focus {
            outline: none;
            border-color: var(--primary-blue);
            box-shadow: 0 0 0 3px rgba(66, 140, 224, 0.1);
        }
        
        .select {
            appearance: none;
            background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
            background-position: right 0.75rem center;
            background-repeat: no-repeat;
            background-size: 1.5em 1.5em;
            padding-right: 2.5rem;
        }
        
        /* Card Components */
        .card {
            background: var(--white);
            border-radius: var(--radius-xl);
            padding: var(--space-6);
            box-shadow: var(--shadow-md);
            border: 1px solid var(--gray-200);
            margin-bottom: var(--space-4);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }
        
        .card-header {
            border-bottom: 1px solid var(--gray-200);
            padding-bottom: var(--space-4);
            margin-bottom: var(--space-4);
        }
        
        .card-title {
            font-size: var(--text-xl);
            font-weight: 600;
            color: var(--gray-800);
        }
        
        .card-gradient {
            background: var(--gradient-primary);
            color: var(--white);
        }
        
        .card-gradient .card-title {
            color: var(--white);
        }
        
        /* Status Badges */
        .badge {
            display: inline-flex;
            align-items: center;
            padding: var(--space-1) var(--space-3);
            font-size: var(--text-xs);
            font-weight: 600;
            border-radius: var(--radius-full);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .badge-success {
            background-color: #D1FAE5;
            color: #065F46;
        }
        
        .badge-warning {
            background-color: #FEF3C7;
            color: #92400E;
        }
        
        .badge-danger {
            background-color: #FEE2E2;
            color: #991B1B;
        }
        
        .badge-info {
            background-color: var(--primary-blue-pale);
            color: var(--primary-blue-dark);
        }
        
        .badge-premium {
            background: var(--gradient-primary);
            color: var(--white);
        }
        
        /* Layout Grid */
        .grid {
            display: grid;
            gap: var(--space-6);
        }
        
        .grid-2 {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .grid-3 {
            grid-template-columns: repeat(3, 1fr);
        }
        
        .grid-4 {
            grid-template-columns: repeat(4, 1fr);
        }
        
        @media (max-width: 768px) {
            .grid-2, .grid-3, .grid-4 {
                grid-template-columns: 1fr;
            }
        }
        
        /* Component Examples Section */
        .examples-section {
            margin: var(--space-12) 0;
        }
        
        .component-showcase {
            background: var(--white);
            border-radius: var(--radius-xl);
            padding: var(--space-8);
            margin: var(--space-6) 0;
            border: 1px solid var(--gray-200);
            box-shadow: var(--shadow-md);
        }
        
        .showcase-title {
            font-size: var(--text-2xl);
            font-weight: 600;
            color: var(--gray-800);
            margin-bottom: var(--space-6);
            padding-bottom: var(--space-3);
            border-bottom: 2px solid var(--gray-200);
        }
        
        .button-group {
            display: flex;
            gap: var(--space-3);
            flex-wrap: wrap;
            margin: var(--space-4) 0;
        }
        
        /* Product Card Example */
        .product-card {
            background: var(--white);
            border-radius: var(--radius-xl);
            overflow: hidden;
            box-shadow: var(--shadow-lg);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid var(--gray-200);
        }
        
        .product-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
        }
        
        .product-image {
            height: 200px;
            background: var(--gradient-primary);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--white);
            font-size: var(--text-3xl);
            font-weight: 700;
        }
        
        .product-content {
            padding: var(--space-6);
        }
        
        .product-title {
            font-size: var(--text-xl);
            font-weight: 600;
            color: var(--gray-800);
            margin-bottom: var(--space-2);
        }
        
        .product-description {
            color: var(--gray-600);
            margin-bottom: var(--space-4);
            line-height: 1.6;
        }
        
        .product-price {
            font-size: var(--text-2xl);
            font-weight: 700;
            color: var(--primary-blue);
            margin-bottom: var(--space-4);
        }
        
        /* Testimonial Card */
        .testimonial-card {
            background: var(--white);
            border-radius: var(--radius-xl);
            padding: var(--space-6);
            border-left: 4px solid var(--primary-magenta);
            box-shadow: var(--shadow-md);
        }
        
        .testimonial-quote {
            font-style: italic;
            color: var(--gray-700);
            margin-bottom: var(--space-4);
            font-size: var(--text-lg);
            line-height: 1.6;
        }
        
        .testimonial-author {
            font-weight: 600;
            color: var(--gray-800);
        }
        
        .testimonial-role {
            color: var(--gray-500);
            font-size: var(--text-sm);
        }
        
        /* Navigation Menu */
        .nav-menu {
            display: flex;
            gap: var(--space-6);
            align-items: center;
            background: var(--white);
            padding: var(--space-4) var(--space-6);
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow-md);
        }
        
        .nav-link {
            color: var(--gray-600);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s ease;
            position: relative;
        }
        
        .nav-link:hover {
            color: var(--primary-blue);
        }
        
        .nav-link.active {
            color: var(--primary-blue);
        }
        
        .nav-link.active::after {
            content: '';
            position: absolute;
            bottom: -8px;
            left: 0;
            right: 0;
            height: 2px;
            background: var(--primary-blue);
            border-radius: var(--radius-full);
        }
        
        /* Hero Section Example */
        .hero-section {
            background: var(--gradient-primary);
            color: var(--white);
            padding: var(--space-16) var(--space-6);
            border-radius: var(--radius-2xl);
            text-align: center;
            margin: var(--space-8) 0;
        }
        
        .hero-title {
            font-size: var(--text-5xl);
            font-weight: 800;
            margin-bottom: var(--space-4);
            line-height: 1.1;
        }
        
        .hero-subtitle {
            font-size: var(--text-xl);
            margin-bottom: var(--space-8);
            opacity: 0.9;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* Feature Grid */
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: var(--space-6);
            margin: var(--space-8) 0;
        }
        
        .feature-card {
            background: var(--white);
            padding: var(--space-6);
            border-radius: var(--radius-xl);
            box-shadow: var(--shadow-md);
            text-align: center;
            border: 1px solid var(--gray-200);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
        }
        
        .feature-icon {
            width: 60px;
            height: 60px;
            background: var(--primary-blue-pale);
            border-radius: var(--radius-full);
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto var(--space-4) auto;
            font-size: var(--text-2xl);
            color: var(--primary-blue);
        }
        
        .feature-title {
            font-size: var(--text-lg);
            font-weight: 600;
            color: var(--gray-800);
            margin-bottom: var(--space-2);
        }
        
        .feature-description {
            color: var(--gray-600);
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1 class="heading-1">JPeptics Design System</h1>
            <p class="body-large">A comprehensive design system for nootropics and supplements, built on competitive analysis of leading brands in the cognitive enhancement and wellness industry.</p>
        </header>

        <section>
            <h2 class="heading-2">Brand Colors</h2>
            <p class="body-base">JPeptics brand colors combine trust-building blue with energetic magenta, reflecting both scientific credibility and vitality.</p>
            
            <h3 class="heading-3">Primary Brand Colors</h3>
            <div class="color-grid">
                <div class="color-card">
                    <div class="color-swatch" style="background-color: #428ce0;"></div>
                    <div class="color-name">Primary Blue</div>
                    <div class="color-value">#428ce0</div>
                    <div class="color-description">Main brand color - trust, cognitive enhancement, professionalism</div>
                </div>
                <div class="color-card">
                    <div class="color-swatch" style="background-color: #3574c4;"></div>
                    <div class="color-name">Primary Blue Dark</div>
                    <div class="color-value">#3574c4</div>
                    <div class="color-description">Hover states and depth</div>
                </div>
                <div class="color-card">
                    <div class="color-swatch" style="background-color: #e8f2fd;"></div>
                    <div class="color-name">Primary Blue Pale</div>
                    <div class="color-value">#e8f2fd</div>
                    <div class="color-description">Background tints and subtle accents</div>
                </div>
            </div>

            <div class="color-grid">
                <div class="color-card">
                    <div class="color-swatch" style="background-color: #e344aa;"></div>
                    <div class="color-name">Primary Magenta</div>
                    <div class="color-value">#e344aa</div>
                    <div class="color-description">Energy, vitality, call-to-action accent</div>
                </div>
                <div class="color-card">
                    <div class="color-swatch" style="background-color: #cc3d9a;"></div>
                    <div class="color-name">Primary Magenta Dark</div>
                    <div class="color-value">#cc3d9a</div>
                    <div class="color-description">Hover states and active elements</div>
                </div>
                <div class="color-card">
                    <div class="color-swatch" style="background-color: #fdeaf7;"></div>
                    <div class="color-name">Primary Magenta Pale</div>
                    <div class="color-value">#fdeaf7</div>
                    <div class="color-description">Background highlights and gentle accents</div>
                </div>
            </div>

            <h3 class="heading-3">Secondary Colors - Health & Wellness</h3>
            <div class="color-grid">
                <div class="color-card">
                    <div class="color-swatch" style="background-color: #10B981;"></div>
                    <div class="color-name">Wellness Green</div>
                    <div class="color-value">#10B981</div>
                    <div class="color-description">Health, natural ingredients, success states</div>
                </div>
                <div class="color-card">
                    <div class="color-swatch" style="background-color: #8B5CF6;"></div>
                    <div class="color-name">Premium Purple</div>
                    <div class="color-value">#8B5CF6</div>
                    <div class="color-description">Premium products, luxury feel</div>
                </div>
                <div class="color-card">
                    <div class="color-swatch" style="background-color: #F59E0B;"></div>
                    <div class="color-name">Energy Orange</div>
                    <div class="color-value">#F59E0B</div>
                    <div class="color-description">Energy, vitamins, warning states</div>
                </div>
                <div class="color-card">
                    <div class="color-swatch" style="background-color: #06B6D4;"></div>
                    <div class="color-name">Refreshing Teal</div>
                    <div class="color-value">#06B6D4</div>
                    <div class="color-description">Refreshing, hydration, cognitive clarity</div>
                </div>
            </div>

            <h3 class="heading-3">System Colors</h3>
            <div class="color-grid">
                <div class="color-card">
                    <div class="color-swatch" style="background-color: #22C55E;"></div>
                    <div class="color-name">Success</div>
                    <div class="color-value">#22C55E</div>
                    <div class="color-description">Order confirmed, in stock</div>
                </div>
                <div class="color-card">
                    <div class="color-swatch" style="background-color: #F59E0B;"></div>
                    <div class="color-name">Warning</div>
                    <div class="color-value">#F59E0B</div>
                    <div class="color-description">Low stock, pending review</div>
                </div>
                <div class="color-card">
                    <div class="color-swatch" style="background-color: #EF4444;"></div>
                    <div class="color-name">Danger</div>
                    <div class="color-value">#EF4444</div>
                    <div class="color-description">Out of stock, errors</div>
                </div>
                <div class="color-card">
                    <div class="color-swatch" style="background-color: #3B82F6;"></div>
                    <div class="color-name">Info</div>
                    <div class="color-value">#3B82F6</div>
                    <div class="color-description">Product information, tips</div>
                </div>
            </div>
        </section>

        <section class="examples-section">
            <h2 class="heading-2">Typography Scale</h2>
            <p class="body-base">Professional, scientific typography using <strong>Roboto</strong> (primary) and <strong>Source Sans Pro</strong> (secondary). These fonts convey authority, trust, and scientific credibility - essential for the nootropics industry.</p>
            
            <div style="background: var(--gray-100); padding: var(--space-4); border-radius: var(--radius-lg); margin: var(--space-4) 0;">
                <h4 class="heading-4">Why These Fonts Work for Nootropics:</h4>
                <ul class="body-base" style="margin-left: var(--space-4); line-height: 1.7;">
                    <li><strong>Roboto:</strong> Google's flagship font, used in Android and professional applications. Clean, geometric, authoritative without being cold.</li>
                    <li><strong>Source Sans Pro:</strong> Adobe's first open-source font, designed for user interfaces and professional content. Highly readable, serious tone.</li>
                    <li><strong>Medical credibility:</strong> Both fonts are widely used in healthcare, pharmaceutical, and scientific contexts.</li>
                    <li><strong>Trust building:</strong> Professional appearance helps establish credibility with customers considering cognitive enhancement products.</li>
                </ul>
            </div>
            
            <div class="component-showcase">
                <h1 class="heading-1">Heading 1 - Hero Titles & Main Headlines</h1>
                <h2 class="heading-2">Heading 2 - Section Headers & Product Names</h2>
                <h3 class="heading-3">Heading 3 - Subsections & Category Titles</h3>
                <h4 class="heading-4">Heading 4 - Component Titles & Features</h4>
                <h5 class="heading-5">Heading 5 - Card Titles & Small Sections</h5>
                <p class="body-large">Body Large - Important descriptions, product benefits, key information</p>
                <p class="body-base">Body Base - Standard paragraph text for general content and product descriptions</p>
                <p class="body-small">Body Small - Supporting text, disclaimers, secondary information</p>
                <p class="caption">Caption - Labels, metadata, image captions</p>
                <p class="text-gradient">Gradient Text - Special highlights and premium features</p>
            </div>

            <div class="component-showcase">
                <div class="showcase-title">Alternative Professional Font Options</div>
                <div class="grid grid-2">
                    <div class="card">
                        <h4 class="heading-4">Most Professional</h4>
                        <ul class="body-base" style="margin-left: var(--space-4); line-height: 1.6;">
                            <li><strong>Roboto</strong> - Google's flagship, very authoritative</li>
                            <li><strong>Source Sans Pro</strong> - Adobe's professional standard</li>
                            <li><strong>Lato</strong> - Medical-grade, clean minimal</li>
                            <li><strong>Open Sans</strong> - Versatile, widely trusted</li>
                        </ul>
                    </div>
                    <div class="card">
                        <h4 class="heading-4">Modern but Serious</h4>
                        <ul class="body-base" style="margin-left: var(--space-4); line-height: 1.6;">
                            <li><strong>Work Sans</strong> - Technical, professional</li>
                            <li><strong>DM Sans</strong> - Serious geometric sans</li>
                            <li><strong>Plus Jakarta Sans</strong> - Modern, authoritative</li>
                            <li><strong>Outfit</strong> - Clean, contemporary</li>
                        </ul>
                    </div>
                </div>
                <p class="body-small" style="margin-top: var(--space-4); color: var(--gray-500);">
                    <strong>Current pairing:</strong> Roboto + Source Sans Pro provides the perfect balance of authority and readability for nootropics/supplements.
                </p>
            </div>
        </section>

        <section class="examples-section">
            <h2 class="heading-2">Component Library</h2>
            
            <div class="component-showcase">
                <div class="showcase-title">Buttons - Action-Oriented Design</div>
                <div class="button-group">
                    <button class="button button-primary button-lg">Shop Nootropics</button>
                    <button class="button button-secondary button-lg">Learn More</button>
                    <button class="button button-gradient button-lg">Try Premium</button>
                </div>
                <div class="button-group">
                    <button class="button button-primary">Add to Cart</button>
                    <button class="button button-secondary">View Details</button>
                    <button class="button button-success">In Stock</button>
                    <button class="button button-warning">Low Stock</button>
                    <button class="button button-danger">Out of Stock</button>
                </div>
                <div class="button-group">
                    <button class="button button-outline">Subscribe & Save</button>
                    <button class="button button-ghost">Compare Products</button>
                    <button class="button button-primary button-sm">Quick Buy</button>
                </div>
            </div>

            <div class="component-showcase">
                <div class="showcase-title">Status Badges</div>
                <div class="button-group">
                    <span class="badge badge-success">Clinically Tested</span>
                    <span class="badge badge-info">Best Seller</span>
                    <span class="badge badge-premium">Premium Formula</span>
                    <span class="badge badge-warning">Limited Edition</span>
                    <span class="badge badge-danger">Final Sale</span>
                </div>
            </div>

            <div class="component-showcase">
                <div class="showcase-title">Form Components</div>
                <div class="grid grid-2">
                    <div class="input-group">
                        <label class="input-label">Email Address</label>
                        <input type="email" class="input" placeholder="your@email.com">
                    </div>
                    <div class="input-group">
                        <label class="input-label">Product Category</label>
                        <select class="input select">
                            <option>Nootropics</option>
                            <option>Cognitive Enhancers</option>
                            <option>Memory Support</option>
                            <option>Focus Boosters</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label class="input-label">Dosage Preference</label>
                        <select class="input select">
                            <option>Beginner (Low dose)</option>
                            <option>Intermediate (Standard)</option>
                            <option>Advanced (High potency)</option>
                        </select>
                    </div>
                    <div class="input-group">
                        <label class="input-label">Subscription Frequency</label>
                        <select class="input select">
                            <option>Monthly</option>
                            <option>Every 2 months</option>
                            <option>Every 3 months</option>
                            <option>One-time purchase</option>
                        </select>
                    </div>
                </div>
            </div>
        </section>

        <section class="examples-section">
            <h2 class="heading-2">E-commerce Layout Examples</h2>
            
            <div class="component-showcase">
                <div class="showcase-title">Navigation Menu</div>
                <nav class="nav-menu">
                    <a href="#" class="nav-link active">Home</a>
                    <a href="#" class="nav-link">Products</a>
                    <a href="#" class="nav-link">Science</a>
                    <a href="#" class="nav-link">Reviews</a>
                    <a href="#" class="nav-link">Support</a>
                    <button class="button button-primary button-sm">Get Started</button>
                </nav>
            </div>

            <div class="component-showcase">
                <div class="showcase-title">Hero Section</div>
                <div class="hero-section">
                    <h1 class="hero-title">Unlock Your Cognitive Potential</h1>
                    <p class="hero-subtitle">Premium nootropics backed by science, designed to enhance focus, memory, and mental clarity for peak performance.</p>
                    <div class="button-group">
                        <button class="button button-secondary button-lg">Shop Now</button>
                        <button class="button button-outline button-lg" style="border-color: white; color: white;">Learn More</button>
                    </div>
                </div>
            </div>

            <div class="component-showcase">
                <div class="showcase-title">Product Cards</div>
                <div class="grid grid-3">
                    <div class="product-card">
                        <div class="product-image">💊</div>
                        <div class="product-content">
                            <span class="badge badge-premium">Premium</span>
                            <h3 class="product-title">Focus Pro</h3>
                            <p class="product-description">Advanced nootropic blend for enhanced concentration and mental clarity.</p>
                            <div class="product-price">$49.99</div>
                            <button class="button button-primary" style="width: 100%;">Add to Cart</button>
                        </div>
                    </div>
                    <div class="product-card">
                        <div class="product-image">🧠</div>
                        <div class="product-content">
                            <span class="badge badge-success">Best Seller</span>
                            <h3 class="product-title">Memory Max</h3>
                            <p class="product-description">Scientifically formulated to support memory formation and recall.</p>
                            <div class="product-price">$39.99</div>
                            <button class="button button-primary" style="width: 100%;">Add to Cart</button>
                        </div>
                    </div>
                    <div class="product-card">
                        <div class="product-image">⚡</div>
                        <div class="product-content">
                            <span class="badge badge-info">New</span>
                            <h3 class="product-title">Energy Boost</h3>
                            <p class="product-description">Natural energy enhancement without jitters or crashes.</p>
                            <div class="product-price">$29.99</div>
                            <button class="button button-primary" style="width: 100%;">Add to Cart</button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="component-showcase">
                <div class="showcase-title">Feature Highlights</div>
                <div class="feature-grid">
                    <div class="feature-card">
                        <div class="feature-icon">🔬</div>
                        <h3 class="feature-title">Clinically Tested</h3>
                        <p class="feature-description">All ingredients backed by peer-reviewed research and clinical studies for safety and efficacy.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">🌿</div>
                        <h3 class="feature-title">Natural Ingredients</h3>
                        <p class="feature-description">Premium plant-based compounds sourced from trusted suppliers worldwide.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">🚚</div>
                        <h3 class="feature-title">Fast Shipping</h3>
                        <p class="feature-description">Free 2-day shipping on orders over $50, with discrete packaging for privacy.</p>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">💯</div>
                        <h3 class="feature-title">Money-Back Guarantee</h3>
                        <p class="feature-description">30-day satisfaction guarantee. Not happy? Get your money back, no questions asked.</p>
                    </div>
                </div>
            </div>

            <div class="component-showcase">
                <div class="showcase-title">Customer Testimonials</div>
                <div class="grid grid-2">
                    <div class="testimonial-card">
                        <p class="testimonial-quote">"JPeptics transformed my daily productivity. I can focus for hours without the afternoon crash I used to experience with coffee."</p>
                        <div class="testimonial-author">Sarah Chen</div>
                        <div class="testimonial-role">Software Engineer</div>
                    </div>
                    <div class="testimonial-card">
                        <p class="testimonial-quote">"As a medical student, I need all the cognitive support I can get. These supplements have become an essential part of my study routine."</p>
                        <div class="testimonial-author">Marcus Rodriguez</div>
                        <div class="testimonial-role">Medical Student</div>
                    </div>
                </div>
            </div>
        </section>

        <section class="examples-section">
            <h2 class="heading-2">Design Principles & Guidelines</h2>
            
            <div class="component-showcase">
                <div class="showcase-title">Spacing System - 8px Grid</div>
                <p class="body-base">All spacing follows an 8px grid for consistency and visual rhythm:</p>
                <ul class="body-base" style="margin-left: var(--space-6); margin-top: var(--space-4); line-height: 1.8;">
                    <li><strong>4px (space-1):</strong> Tight spacing between related elements, button padding</li>
                    <li><strong>8px (space-2):</strong> Small gaps, icon spacing, badge padding</li>
                    <li><strong>16px (space-4):</strong> Standard component padding, form field spacing</li>
                    <li><strong>24px (space-6):</strong> Card padding, section spacing</li>
                    <li><strong>32px (space-8):</strong> Large component spacing</li>
                    <li><strong>64px (space-16):</strong> Major page sections, hero padding</li>
                </ul>
            </div>

            <div class="component-showcase">
                <div class="showcase-title">Industry-Specific Design Patterns</div>
                <div class="grid grid-2">
                    <div class="card">
                        <h4 class="heading-4">Trust Building</h4>
                        <ul class="body-base" style="margin-left: var(--space-4); line-height: 1.6;">
                            <li>Scientific badges and certifications</li>
                            <li>Third-party testing indicators</li>
                            <li>Doctor endorsements</li>
                            <li>Research citations</li>
                            <li>Money-back guarantees</li>
                        </ul>
                    </div>
                    <div class="card">
                        <h4 class="heading-4">Conversion Optimization</h4>
                        <ul class="body-base" style="margin-left: var(--space-4); line-height: 1.6;">
                            <li>Clear benefit-focused messaging</li>
                            <li>Prominent call-to-action buttons</li>
                            <li>Stock level indicators</li>
                            <li>Subscription incentives</li>
                            <li>Social proof and reviews</li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="component-showcase">
                <div class="showcase-title">Accessibility & Performance</div>
                <div class="grid grid-2">
                    <div class="card">
                        <h4 class="heading-4">Accessibility Features</h4>
                        <ul class="body-base" style="margin-left: var(--space-4); line-height: 1.6;">
                            <li>WCAG 2.1 AA compliant color contrast</li>
                            <li>Keyboard navigation support</li>
                            <li>Screen reader optimization</li>
                            <li>Focus indicators on interactive elements</li>
                            <li>Scalable text up to 200%</li>
                        </ul>
                    </div>
                    <div class="card">
                        <h4 class="heading-4">Performance Optimizations</h4>
                        <ul class="body-base" style="margin-left: var(--space-4); line-height: 1.6;">
                            <li>Optimized web fonts (Nunito + Inter)</li>
                            <li>CSS custom properties for theming</li>
                            <li>Minimal external dependencies</li>
                            <li>Progressive enhancement approach</li>
                            <li>Mobile-first responsive design</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <footer style="margin-top: var(--space-16); padding: var(--space-12) 0; border-top: 2px solid var(--gray-200); text-align: center;">
            <h3 class="heading-3 text-gradient">JPeptics Design System</h3>
            <p class="body-base" style="color: var(--gray-500); max-width: 600px; margin: 0 auto;">
                Built for the nootropics and supplements industry, inspired by leading brands like Mind Lab Pro, AG1, Nootropics Depot, and Noom.
                Designed to build trust, drive conversions, and enhance user experience in the cognitive enhancement space.
            </p>
            <div style="margin-top: var(--space-6);">
                <span class="badge badge-info">Science-Backed Design</span>
                <span class="badge badge-success">Conversion Optimized</span>
                <span class="badge badge-premium">Premium Experience</span>
            </div>
        </footer>
    </div>
</body>
</html>
