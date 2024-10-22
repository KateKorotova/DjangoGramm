# DjangoGramm
DjangoGramm is a simple social networking web application built with Django. It allows users to register, log in, and manage their profiles. Users can upload avatars, write a bio, and interact with the platform. This project showcases core Django functionality, including user authentication, email verification, and basic CRUD operations.

## Features
### User Authentication
Sign up, log in, and log out functionality.
### Email Confirmation
Users must verify their email via a unique confirmation link.
### Profile Management
Users can upload avatars, add bio, and update their profile information.
### Secure Authentication
CSRF tokens for form submission and password hashing.
### Admin Panel
Manage users via Django’s built-in admin interface.

## Installation
### Prerequisites
- Python 3.7 or higher
- Django 4.0 or higher
- SQLite (default), but you can switch to PostgreSQL or MySQL if needed
  
## Steps to Install Locally
### Clone the repository:
```
git clone https://github.com/your-username/DjangoGramm.git
cd DjangoGramm
```
### Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```
### Install the required dependencies:
```
pip install -r requirements.txt
```
### Set up the database:

Make sure you have Django’s default SQLite database or set up your own database.
Run migrations to initialize the database:
```
python manage.py migrate
```
### Create a superuser (optional, for admin access):
```
python manage.py createsuperuser
```
### Run the development server:
```
python manage.py runserver
```
## Access the application:

* Visit http://127.0.0.1:8000/ in your browser.
* The admin panel is available at http://127.0.0.1:8000/admin/.

## Usage
### Registering a New User
1. Visit the Sign Up page and enter your details (email, password, full name).
2. A confirmation email will be sent with a unique link to verify your account.
3. After email confirmation, you will be redirected to the login page.
### Logging In
- Use your credentials to log in to the platform and access the home page.
### Admin Panel
- You can manage users, their profiles, and permissions via the Django Admin panel.

## Project Structure
```
DjangoGramm/
│
├── DjangoGramm/           # Project configuration
│   ├── __init__.py
│   ├── settings.py        # Project settings
│   ├── urls.py            # Project URLs
│   ├── wsgi.py
│
├── users/                 # User app containing core functionality
│   ├── migrations/
│   ├── templates/         # HTML templates
│   ├── __init__.py
│   ├── admin.py           # Django admin configurations
│   ├── apps.py
│   ├── forms.py           # User registration and login forms
│   ├── models.py          # CustomUser model
│   ├── urls.py            # URLs for the user app
│   ├── views.py           # Core views (register, login, logout)
│
├── media/                 # User-uploaded media files (e.g., avatars)
├── static/                # Static files (CSS, JS)
├── manage.py              # Django management script
├── README.md              # Project documentation (this file)
└── requirements.txt       # Project dependencies
```

## Technologies Used
- Django: Backend framework for web application development.
- HTML/CSS: For front-end design and responsive UI.
- Bootstrap: For consistent styling and layout.
- SQLite: Default database (can be changed to PostgreSQL, MySQL, etc.).
- Django Crispy Forms: To style forms easily with Bootstrap.

## Authors and acknowledgment
Author: Yekatierina Korotova
