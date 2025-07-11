# Project Requirements

## Python & Django Packages

- **Django**: Web framework used to build the backend.
- **djangorestframework**: For building RESTful APIs.
- **paypalrestsdk**: To handle PayPal payment integration.
- **psycopg2-binary**: PostgreSQL database adapter.
- **python-decouple**: For handling environment variables.
- **requests**: To make HTTP requests (used in ORS API).
- **gunicorn** *(optional for deployment)*

## Frontend (React/Vite)
- **React**: JavaScript library for building the UI.
- **Axios**: To make API requests to the Django backend.
- **React Router**: For managing frontend routes.
- **Tailwind CSS / Bootstrap**: For styling.

## System Dependencies
- Python 3.10+
- Node.js (for frontend)
- PostgreSQL
- Docker (optional for containerization)

## External APIs
- **OpenRouteService (ORS)**: Used for route planning and distance calculation.
- **PayPal API**: For processing logistics payments online.

## Environment Variables

Store these in a `.env` file:

```bash
SECRET_KEY=your_secret_key_here
DEBUG=True
PAYPAL_CLIENT_ID=your_paypal_client_id
PAYPAL_CLIENT_SECRET=your_paypal_client_secret
ORS_API_KEY=your_openrouteservice_key
DATABASE_URL=postgres://user:pass@host:port/dbname
```

## Apps in the Project

-   `users` – Handles user registration, login, role management (admin, dispatcher, driver,accountant,customer).
-   `orders` – Manages order creation, status, route integration, and assignment.
-   `drivers` – Driver-specific data and availability management.
-   `vehicles` – Vehicle records and availability.
-   `routes` – Route planning via ORS and distance estimations.
-   `trips` – Manages trip assignments of drivers and vehicles.
-   `dispatcher` – lists dispatch task
-   `billing` – Payment processing via PayPal.
-   `customers` - Handles customer login/registration(Not complete yet)
-   `fuel` - maintains vehicle fuel logs
-   `maintanence` - maintains vehicle maintanence records
-   `accountant`-money related report generator
-   `report`-generates pdf,excel reports