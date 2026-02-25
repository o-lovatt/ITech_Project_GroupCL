# Hotel Management System

A web-based Hotel Management System built using Python and Django.  
This application allows guests to search and book rooms, and staff to manage bookings and room availability.

---

## Live Application
Deployed URL: (add your deployed link here)

---

## Repository
GitHub Repository: (add your repo link here)

---

## Tech Stack
- Backend: Python, Django
- Frontend: HTML, CSS, Bootstrap
- Database: SQLite (Development) / PostgreSQL (Production)
- Client-side Interactivity: JavaScript / AJAX
- Deployment: (Render / PythonAnywhere)

---

## Core Features
- User authentication (login/logout)
- Role-based access (Guest/Admin/Receptionist)
- Room availability search
- Booking creation and management
- Admin room management (availability/prices)
- Responsive UI (mobile/tablet/desktop)

---

## Run Locally (Development)

```bash
git clone <YOUR_REPO_LINK>
cd <PROJECT_FOLDER>
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
