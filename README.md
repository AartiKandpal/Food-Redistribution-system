# FoodBridge - Food Redistribution System 🍲🤝

FoodBridge is a responsive web application designed to act as a **digital bridge** between hotels, restaurants, or individual donors and local NGOs. The primary objective of this project is to minimize food wastage and tackle hunger by enabling real-time redistribution of surplus fresh food.

---

## 🚀 Key Features

* **Responsive Donor Dashboard:** A clean user interface for hotels and restaurants to quickly list surplus food details, including item names, quantity (servings), and estimated expiry time.
* **Real-time Map Integration:** Uses OpenStreetMap (OSM) API via Leaflet.js to display exact pickup locations dynamically, helping NGOs navigate easily.
* **Modern Authentication UI:** A sleek, unified Login and Registration system utilizing Bootstrap nav-pills for smooth switching without page reloads.
* **Mobile-First Design:** Built completely using standard Bootstrap layout components, ensuring compatibility across smartphones, tablets, and laptops.

---

## 🛠️ Tech Stack Used

* **Frontend:** HTML5, CSS3
* **Framework:** Bootstrap 5 (for fast, responsive UI elements)
* **Maps API:** OpenStreetMap (OSM) & Leaflet.js (Open-source & cost-effective alternative to Google Maps)
* **Template Engine:** Jinja2 syntax ready for dynamic data rendering (Planned Backend Integration).

---

## 📂 Project Structure

```text
├── index.html       # The main landing page with available food listings and donation form
├── login.html       # Secure unified interface for Donor/NGO sign-in and registration
├── map.html         # Interactive location tracking page powered by Leaflet.js & OSM
└── README.md        # Project documentation
