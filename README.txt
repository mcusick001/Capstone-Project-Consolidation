========================================================================
                      DJANGO NEWS API CAPSTONE PROJECT
========================================================================

1. PROJECT OVERVIEW
-------------------
This project is a comprehensive full-stack News and Content Management Portal
built with Django and Django REST Framework (DRF), backed by a MariaDB relational
database. It features strict Role-Based Access Control (RBAC), custom web dashboards
for readers, journalists, and editors, automated email notifications, and webhook
event handlers.


2. PROJECT STRUCTURE
--------------------
news_project/
│
├── news/
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── templates/
│   │   └── news/
│   │       ├── base.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── editor_dashboard.html
│   │       ├── journalist_dashboard.html
│   │       ├── subscriptions.html
│   │       └── publisher_management.html
│   ├── __init__.py
│   ├── admin.py
│   ├── api_views.py
│   ├── apps.py
│   ├── decorators.py
│   ├── forms.py
│   ├── models.py
│   ├── permissions.py 
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── news_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── .gitignore
├── manage.py
├── README.txt
└── requirements.txt


3. LOCAL SETUP & INSTALLATION
-----------------------------
1. Clone the repository and navigate into the project directory:
   cd news_project

2. Create and activate a Python virtual environment:
   python -m venv venv
   venv\Scripts\Activate.ps1

3. Install required dependencies:
   pip install -r requirements.txt

4. Configure your MariaDB connection details in `news_project/settings.py`.

5. Run database migrations:
   python manage.py migrate

6. Launch the local development server:
   python manage.py runserver


4. AUTOMATED TEST SUITE
-----------------------
The project includes a robust unit test suite (`APITestCase`) in `news/tests.py`
covering authentication, RBAC permissions, webhook mocking, and subscription filtering.

To run the automated tests:
   python manage.py test news
