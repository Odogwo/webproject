
## Building a Blog Application


https://learning.oreilly.com/library/view/django-4-by/9781801813051/Text/Chapter_1.xhtml#_idParaDest-14

1. Installing Python
1. Creating a Python virtual environment
1. Installing Django
1. Creating and configuring a Django project
1. Building a Django application
1. Designing data models
1. Creating and applying model migrations
1. Creating an administration site for your models
1. Working with QuerySets and model managers
1. Building views, templates, and URLs
1. Understanding the Django request/response cycle



### Notes

```
python -m venv my_env
.\my_env\Scripts\activate
```

```
pip install Django~=4.1.0
python -m django --version
```

```
django-admin startproject mysite
cd mysite
python manage.py migrate
python manage.py runserver
```

```
python manage.py startapp blog
```

