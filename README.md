🚚 Smart Fleet Manager
A full-stack web application for intelligent and efficient fleet and logistics management, built with Django, React, and PostgreSQL.

🔧 Tech Stack
Backend: Django, Django REST Framework

Frontend: React.js, Tailwind CSS

Database: PostgreSQL

Auth: JWT (JSON Web Tokens)

Deployment: Render / Railway / Vercel / Netlify (optional)

🌟 Features
🔐 Authentication & Roles
JWT-based secure login and registration

Role-based dashboards for:

Admin

Dispatcher

Customer

Driver

Accountant

🚛 Fleet Management
Vehicle creation & assignment

Driver registration & tracking

Maintenance & fuel log tracking

📦 Order & Dispatch Workflow
Customers create delivery orders

Dispatcher approves, assigns vehicle & driver

Real-time order tracking and status updates

💵 Payments & Accounting
Customer redirected to PayPal for order payments

Accountants access all transaction & order reports

Generate PDF/CSV reports (invoices, logs, expenses)

📍 Location & Monitoring
Geolocation-based updates (optional GPS/device support)

Integration-ready for AI-based driver drowsiness detection

Route optimization (coming soon)

📂 Project Structure
Backend (/backend)
bash
Copy
Edit
/backend
├── core/
│   ├── users/
│   ├── vehicles/
│   ├── orders/
│   ├── drivers/
│   ├── dispatcher/
│   ├── trips/
│   └── accounting/
├── utils/
├── media/
└── manage.py
📌 Future Enhancements
Live GPS integration

AI-based driver behavior analytics

Notifications & alerts (Twilio/Email/SMS)

Fleet performance analytics dashboard

👨‍💻 Author
Anmolsinh M Chudasama
Full Stack Developer | Smart Logistics Enthusiast
GitHub
