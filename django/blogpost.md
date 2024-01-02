
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



### Setups

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

### blog\models.py

> we will define a Post model that will allow us to store blog posts in the database.
```
from django.db import models
class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    def __str__(self):
        return self.title
```

> Add date time field

```
from django.db import models
from django.utils import timezone
class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
```

> Defining a default sort order

```
from django.db import models
from django.utils import timezone
class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-publish']
    def __str__(self):
        return self.title
```

> Adding a database index

```
from django.db import models
from django.utils import timezone
class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    def __str__(self):
        return self.title
```
> activating the application

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
]
```

> Adding a status field
```
from django.db import models
from django.utils import timezone
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    def __str__(self):
        return self.title
```
> shell

```
python manage.py shell

>>> from blog.models import Post
>>> Post.Status.choices
>>> Post.Status.labels
>>> Post.Status.values
>>> Post.Status.names
```

> Adding a many-to-one relationship

```
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
    def __str__(self):
        return self.title
```

> Creating and applying migrations

```
python manage.py makemigrations blog

python manage.py shell
python manage.py sqlmigrate blog 0001

python manage.py migrate
```

> Superuser :Creating an administration site for models

```
python manage.py createsuperuser

Username (leave blank to use 'admin'): admin
Email address: admin@admin.com
Password: ********
Password (again): ********

python manage.py runserver
```

### admin.py
> add models to site

```
from django.contrib import admin
from .models import Post
admin.site.register(Post)
```

> Customizing how models are displayed
```
from django.contrib import admin
from .models import Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
```

> more options
```
from django.contrib import admin
from .models import Post
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
```

### Working with QuerySets and managers

> Creating objects
```
python manage.py shell

>>> from django.contrib.auth.models import User
>>> from blog.models import Post
>>> user = User.objects.get(username='admin')
>>> post = Post(title='Another post',
...             slug='another-post',
...             body='Post body.',
...             author=user)
>>> post.save()

user = User.objects.get(username='admin')
post = Post(title='Another post', slug='another-post', body='Post body.', author=user)
post.save()

Post.objects.create(title='One more post',
                    slug='one-more-post',
                    body='Post body.',
                    author=user)
```

> Updating objects
```
>>> post.title = 'New title'
>>> post.save()
```


> Retrieving objects
```
>>> all_posts = Post.objects.all()
>>> Post.objects.all()
<QuerySet [<Post: Who was Django Reinhardt?>, <Post: New title>]>
```


> Using the filter() method
```
>>> Post.objects.filter(publish__year=2022)
>>> Post.objects.filter(publish__year=2022, author__username='admin')

>>> Post.objects.filter(publish__year=2022) \
>>>             .filter(author__username='admin')
```

> Using exclude()
```
>>> Post.objects.filter(publish__year=2022) \
>>>             .exclude(title__startswith='Why'
```


> Using order_by()
```
>>> Post.objects.order_by('title')
>>> Post.objects.order_by('-title')
```

> Deleting objects
```
>>> post = Post.objects.get(id=1)
>>> post.delete()
```


> When QuerySets are evaluated
```
QuerySets are only evaluated in the following cases:

The first time you iterate over them
When you slice them, for instance, Post.objects.all()[:3]
When you pickle or cache them
When you call repr() or len() on them
When you explicitly call list() on them
When you test them in a statement, such as bool(), or, and, or if
```
### models.py
> Creating model managers
```
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                     .filter(status=Post.Status.PUBLISHED)
class Post(models.Model):
    # model fields
    # ...
    objects = models.Manager() # The default manager.
    published = PublishedManager() # Our custom manager.
    class Meta:
        ordering = ['-publish']
    def __str__(self):
        return self.title
```

>
```
python manage.py shell

>>> from blog.models import Post
>>> Post.published.filter(title__startswith='Who')

```
### views.py

> Building list and detail views - Creating list and detail views
```
from django.shortcuts import render
from .models import Post
def post_list(request):
    posts = Post.published.all()
    return render(request,
                 'blog/post/list.html',
                 {'posts': posts})
```

> Second view to display 
```
from django.http import Http404
def post_detail(request, id):
    try:
        post = Post.published.get(id=id)
    except Post.DoesNotExist:
        raise Http404("No Post found.")
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
```

> Using the get_object_or_404 shortcut
```
from django.shortcuts import render, get_object_or_404
# ...
def post_detail(request, id):
    post = get_object_or_404(Post,
                             id=id,
                             status=Post.Status.PUBLISHED)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
```

### urls.py
> Adding URL patterns for your views
```
from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    # post views
    path('', views.post_list, name='post_list'),
    path('<int:id>/', views.post_detail, name='post_detail'),
]
```

>
```
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls', namespace='blog')),
]
```
### Templates
> structures
```
templates/
    blog/
        base.html
        post/
            list.html
            detail.html

Template tags control the rendering of the template and look like {% tag %}
Template variables get replaced with values when the template is rendered and look like {{ variable }}
Template filters allow you to modify variables for display and look like {{ variable|filter }}

```
### base.html
>
```
{% load static %}
<!DOCTYPE html>
<html>
<head>
  <title>{% block title %}{% endblock %}</title>
  <link href="{% static "css/blog.css" %}" rel="stylesheet">
</head>
<body>
  <div id="content">
    {% block content %}
    {% endblock %}
  </div>
  <div id="sidebar">
    <h2>My blog</h2>
    <p>This is my blog.</p>
  </div>
</body>
</html>
```

### post\list.html
>
```
{% extends "blog/base.html" %}
{% block title %}My Blog{% endblock %}
{% block content %}
  <h1>My Blog</h1>
  {% for post in posts %}
    <h2>
      <a href="{% url 'blog:post_detail' post.id %}">
        {{ post.title }}
      </a>
    </h2>
    <p class="date">
      Published {{ post.publish }} by {{ post.author }}
    </p>
    {{ post.body|truncatewords:30|linebreaks }}
  {% endfor %}
{% endblock %}
```

>
```
python manage.py runserver
```

> post/detail.html
```
{% extends "blog/base.html" %}
{% block title %}{{ post.title }}{% endblock %}
{% block content %}
  <h1>{{ post.title }}</h1>
  <p class="date">
    Published {{ post.publish }} by {{ post.author }}
  </p>
  {{ post.body|linebreaks }}
{% endblock %}
```

>
```

```

>
```

```



