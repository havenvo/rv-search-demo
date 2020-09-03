My first Django Project to demonstrate how to use Django template, Ajax data loading.

# How to import data and run dev server
From a Python virtual environment
cd RvSearch

python manage.py migrate

python manage.py shell

from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()

python manage.py loaddata db.json

Finally, 
python manage.py runserver
Enjoy the app at http://127.0.0.1:8000/

PS: Admin credential
Email: admin@example.com
Password: zxcvbnm@123