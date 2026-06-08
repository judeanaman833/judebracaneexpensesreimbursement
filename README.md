# Django Expense Tracker

A modern, secure Django web application for tracking personal expenses, managing categories, and visualizing spending habits. Built for productivity and insight, this project is perfect for anyone who wants to organize their finances with a clean UI and robust features.

## Features

- **User Authentication:** Secure registration and login system.
- **Expense Management:** Add, edit, delete, and view expenses.
- **Category Management:** Organize expenses by custom categories.
- **Dashboard Analytics:** Interactive charts and summaries of your spending.
- **Responsive UI:** Mobile-friendly design with custom templates.
- **Data Security:** User data is private and protected.

## Tech Stack

- **Backend:** Python 3, Django 5
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite (default, easily swappable)
- **Authentication:** Django built-in auth
- **Visualization:** Chart.js (via custom template tags)

## Installation & Setup

### 1. Clone the Repository

```sh
git clone https://github.com/judeanaman833/judebracaneexpensesreimbursement.git
cd django_expense_tracker
```

### 2. Create and Activate a Virtual Environment

```sh
python -m venv venv
venv\Scripts\activate  # On Windows
# or
source venv/bin/activate  # On Mac/Linux
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root with at least:

```
SECRET_KEY = your-django-secret-key
```

### 5. Apply Migrations

```sh
python manage.py migrate
```

### 6. Create a Superuser (for admin access)

```sh
python manage.py createsuperuser
```

### 7. Run the Development Server

```sh
python manage.py runserver
```

Visit [http://localhost:8000](http://localhost:8000) in your browser.

## Project Structure

```
django_expense_tracker/
├── account/         # User authentication
├── expense_tracker/ # Project settings
├── tracker/         # Expense and category management
├── static/          # Static files (JS)
├── db.sqlite3       # Database
├── manage.py        # Django management script
├── .env             # Environment variables
├── requirements.txt # Python dependencies
```

## Customization

- **Extend Models:** Add more fields to expenses or categories as needed.
- **APIs:** Build REST APIs with Django REST Framework for mobile or integrations.

## Analytics Dashboard

The dashboard provides interactive charts and summaries of your expenses by category and over time.  
Great for personal insight and portfolio demonstration!
