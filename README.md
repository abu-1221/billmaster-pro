# 💼 BillMaster Pro - Professional Billing System

A **complete frontend-only** billing and invoicing system built with **HTML, CSS, and JavaScript**. No backend required — all data is persisted in **localStorage**.

## ✨ Features

- 📊 **Analytics Dashboard** — Real-time sales charts, revenue tracking, and business metrics
- 🧾 **POS Billing** — Professional point-of-sale interface with cart management
- 📋 **Invoice Management** — Create, view, print, and track invoices
- 📦 **Product Management** — Full CRUD for products with categories and stock tracking
- 👥 **Customer Management** — Customer database with order history
- 🏷️ **Category Management** — Organize products by categories
- ⚙️ **Settings** — Business info, billing settings, and user management
- 🔐 **Authentication** — Login system with demo credentials
- 📱 **Responsive Design** — Works on desktop, tablet, and mobile
- 🌙 **Dark Theme** — Premium dark UI with glassmorphism effects

## 🚀 Getting Started

### Option 1: Direct File Open

Simply open `static/login.html` in your web browser.

### Option 2: Using a Local Server (Recommended)

```bash
# Using Python
cd static
python -m http.server 8080

# Using Node.js
npx serve static

# Using VS Code
# Install "Live Server" extension and open static/login.html
```

Then open `http://localhost:8080` in your browser.

## 🔑 Demo Credentials

| Username | Password   | Role  |
| -------- | ---------- | ----- |
| `admin`  | `admin123` | Admin |
| `staff`  | `staff123` | Staff |

## 📁 Project Structure

```
billmaster-pro-master/
├── index.html              # Root redirect
├── README.md               # This file
└── static/
    ├── index.html          # Redirect to login
    ├── login.html          # Login page
    ├── dashboard.html      # Analytics dashboard
    ├── billing.html        # POS billing interface
    ├── invoices.html       # Invoice management
    ├── products.html       # Product management
    ├── customers.html      # Customer management
    ├── categories.html     # Category management
    ├── settings.html       # App settings
    └── assets/
        ├── css/
        │   ├── style.css   # Design system & components
        │   ├── layout.css  # Sidebar & header layout
        │   └── billing.css # POS billing styles
        └── js/
            └── app.js      # Complete application logic (localStorage)
```

## 💡 How It Works

- All data (products, customers, invoices, settings) is stored in the browser's **localStorage**
- On first load, the app automatically seeds with **sample data** (24 products, 5 customers, 30 days of invoices)
- All operations (CRUD, analytics, authentication) run entirely in the browser
- Data persists across page refreshes but is browser-specific

## 🎨 Tech Stack

- **HTML5** — Semantic structure
- **CSS3** — Custom design system with CSS variables, glassmorphism, animations
- **JavaScript** — Vanilla JS with localStorage-based state management
- **Chart.js** — Dashboard analytics charts
- **Google Fonts** — Inter typeface

## 📝 Notes

- To reset all data, open browser console and run: `localStorage.clear()` then refresh
- Data is stored per-browser; clearing browser data will reset the app
- The app works offline after the first load (except Google Fonts and Chart.js CDN)
