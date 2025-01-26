# Django REST Framework TodoApp

Clone the Repository

Create venv:
    .\venv\scripts\activate

Install the necessary dependencies:
    pip install -r requirements.txt

Run the following command to apply the database migrations:
    python manage.py migrate

Create a superuser to access the Django admin interface: 
    python manage.py createsuperuser

Run the Django development server:

    python manage.py runserver

Once the server is running, you can access the following endpoints:

    Admin Panel: http://127.0.0.1:8000/admin/

    Todo API: http://127.0.0.1:8000/todos/


You can access the documentation at the following URL:

    http://127.0.0.1:8000/swagger/