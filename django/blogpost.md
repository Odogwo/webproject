
# Building a Blog Application


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
### post/detail.html
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
python manage.py runserver
/blog/1/.
```
## Using canonical URLs for models

> import the reverse() function and add the get_absolute_url() method to the Post model
```
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
                     .filter(status=Post.Status.PUBLISHED)
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
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.id])
```

### blog/post/list.html
> replace <a href="{% url 'blog:post_detail' post.id %}">
```
{% extends "blog/base.html" %}
{% block title %}My Blog{% endblock %}
{% block content %}
  <h1>My Blog</h1>
  {% for post in posts %}
    <h2>
      <a href="{{ post.get_absolute_url }}">
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
models.py
> Creating SEO-friendly URLs for posts
> add the following unique_for_date parameter to the slug field of the Post model:
```
class Post(models.Model):
    # ...
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    # ...
```

> run
```
python manage.py makemigrations blog
python manage.py migrate

```
### blog/urls.py
> Modifying the URL patterns
> the urls.py file path('<int:id>/', views.post_detail, name='post_detail'),
```
from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    # Post views
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
]
```
post/detail.py
> Modifying the views
```
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
```
models.py
> Modifying the canonical URL for posts
> edit the get_absolute_url()
```
class Post(models.Model):
    # ...
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
```

>
```
python manage.py runserver
```

>
```
python manage.py runserver
/blog/2022/1/1/who-was-django-reinhardt/.
```
### views.py
> Adding pagination
```
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator
def post_list(request):
    post_list = Post.published.all()
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)
    return render(request,
                  'blog/post/list.html',
                  {'posts': posts})
```
### templates/pagination.html

>
```
<div class="pagination">
  <span class="step-links">
    {% if page.has_previous %}
      <a href="?page={{ page.previous_page_number }}">Previous</a>
    {% endif %}
    <span class="current">
      Page {{ page.number }} of {{ page.paginator.num_pages }}.
    </span>
    {% if page.has_next %}
      <a href="?page={{ page.next_page_number }}">Next</a>
    {% endif %}
  </span>
</div>
```
### blog/post/list.html
>
```
{% extends "blog/base.html" %}
{% block title %}My Blog{% endblock %}
{% block content %}
  <h1>My Blog</h1>
  {% for post in posts %}
    <h2>
      <a href="{{ post.get_absolute_url }}">
        {{ post.title }}
      </a>
    </h2>
    <p class="date">
      Published {{ post.publish }} by {{ post.author }}
    </p>
    {{ post.body|truncatewords:30|linebreaks }}
  {% endfor %}
  {% include "pagination.html" with page=posts %}
{% endblock %}
```
>
```
python manage.py runserver

http://127.0.0.1:8000/admin/blog/post/
http://127.0.0.1:8000/blog/
```
### blog/ views.py 
> Handling pagination errors
> http://127.0.0.1:8000/blog/?page=3 i
```
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage
def post_list(request):
    post_list = Post.published.all()
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                   {'posts': posts})
```
>
```
http://127.0.0.1:8000/blog/?page=3
```
>http://127.0.0.1:8000/blog/?page=asdf
```
from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
def post_list(request):
    post_list = Post.published.all()
    # Pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page')
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request,
                  'blog/post/list.html',
                   {'posts': posts})
```
> 
```
http://127.0.0.1:8000/blog/?page=asdf
```

### blog/views.py
> Building class-based views
> Using a class-based view to list posts
```
from django.views.generic import ListView
class PostListView(ListView):
    """
    Alternative post list view
    """
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'
```
### blog/urls.py
> 
```
urlpatterns = [
    # Post views
    # path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail,
        name='post_detail'),
]
```
###  post/list.html
>
```
{% extends "blog/base.html" %}
{% block title %}My Blog{% endblock %}
{% block content %}
  <h1>My Blog</h1>
  {% for post in posts %}
    <h2>
      <a href="{{ post.get_absolute_url }}">
        {{ post.title }}
      </a>
    </h2>
    <p class="date">
      Published {{ post.publish }} by {{ post.author }}
    </p>
    {{ post.body|truncatewords:30|linebreaks }}
  {% endfor %}
  {% include "pagination.html" with page=page_obj %}
{% endblock %}
```

>
```
http://127.0.0.1:8000/blog/
```

forms.py
> Recommending posts by email
> Creating forms with Django
```
from django import forms
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)
```

blog/views.py
> Handling forms in views
> 
```
from .forms import EmailPostForm
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form})
```

### settings
> Sending emails with Django
> 
```
# Email server configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your_account@gmail.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

> testingb
```
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
>
```
Open https://myaccount.google.com/ in your browser.
https://learning.oreilly.com/library/view/django-4-by/9781801813051/Text/Chapter_2.xhtml#_idParaDest-81
```

>
```
# Email server configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'your_account@gmail.com'
EMAIL_HOST_PASSWORD = 'xxxxxxxxxxxxxxxx'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```
>
```
python manage.py shell

>>> from django.core.mail import send_mail
>>> send_mail('Django mail',
...           'This e-mail was sent with Django.',
...           'your_account@gmail.com',
...           ['your_account@gmail.com'],
...           fail_silently=False)
```

### blog/views.py
> Sending emails in views
```
from django.core.mail import send_mail
def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                      f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'your_account@gmail.com',
                      [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


```


>
```
Replace your_account@gmail.com with your real email account
 if you are using an SMTP server instead of console.EmailBackend.
```

### blog/urls.py

>
```
from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    # Post views
    # path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    path('<int:post_id>/share/',
         views.post_share, name='post_share'),
]
```
### blog/templates/blog/post/ share.html
>
```
{% extends "blog/base.html" %}
{% block title %}Share a post{% endblock %}
{% block content %}
  {% if sent %}
    <h1>E-mail successfully sent</h1>
    <p>
      "{{ post.title }}" was successfully sent to {{ form.cleaned_data.to }}.
    </p>
  {% else %}
    <h1>Share "{{ post.title }}" by e-mail</h1>
    <form method="post">
      {{ form.as_p }}
      {% csrf_token %}
      <input type="submit" value="Send e-mail">
    </form>
  {% endif %}
{% endblock %}
```
### blog/post/detail.html
>
```
{% extends "blog/base.html" %}
{% block title %}{{ post.title }}{% endblock %}
{% block content %}
  <h1>{{ post.title }}</h1>
  <p class="date">
    Published {{ post.publish }} by {{ post.author }}
  </p>
  {{ post.body|linebreaks }}
  <p>
    <a href="{% url "blog:post_share" post.id %}">
      Share this post
    </a>
  </p>
{% endblock %}
```

>
```
python manage.py runserver
```
### models.py
> Creating a comment system
> Creating a model for comments
```
class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


```
### models.py
>
```
python manage.py makemigrations blog

python manage.py migrate
```

>
```
from .models import Post, Comment
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body'
```

>
```
python manage.py runserver

Open http://127.0.0.1:8000/admin/
```
### blog/forms.py
> Creating forms from models
```
from .models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
```
### blog /views.py 
>
```
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage,\
                                  PageNotAnInteger
from django.views.generic import ListView
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
# ...
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request, 'blog/post/comment.html',
                           {'post': post,
                            'form': form,
                            'comment': comment})

```
### blog/urls.py
>
```
from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    # Post views
    # path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail,
         name='post_detail'),
    path('<int:post_id>/share/',
         views.post_share, name='post_share'),
    path('<int:post_id>/comment/',
         views.post_comment, name='post_comment'),
]
```
### template 
>
```
templates/
  blog/
    post/
      includes/
        comment_form.html
      detail.html
      list.html
      share.html
```
### blog/post/includes/comment_form.html
>
```
<h2>Add a new comment</h2>
<form action="{% url "blog:post_comment" post.id %}" method="post">
  {{ form.as_p }}
  {% csrf_token %}
  <p><input type="submit" value="Add comment"></p>
</form>
```

### templates/blog/post/comment.html
>
```
templates/
  blog/
    post/
      includes/
        comment_form.html
      comment.html
      detail.html
      list.html
      share.html
```

### blog/post/comment.html
>
```
{% extends "blog/base.html" %}
{% block title %}Add a comment{% endblock %}
{% block content %}
  {% if comment %}
    <h2>Your comment has been added.</h2>
    <p><a href="{{ post.get_absolute_url }}">Back to the post</a></p>
  {% else %}
    {% include "blog/post/includes/comment_form.html" %}
  {% endif %}
{% endblock %}
```

### views.py
>
```
def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    # List of active comments for this post
    comments = post.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})
```
### blog/post/detail.html
>
```
{% extends "blog/base.html" %}
{% block title %}{{ post.title }}{% endblock %}
{% block content %}
  <h1>{{ post.title }}</h1>
  <p class="date">
    Published {{ post.publish }} by {{ post.author }}
  </p>
  {{ post.body|linebreaks }}
  <p>
    <a href="{% url "blog:post_share" post.id %}">
      Share this post
    </a>
  </p>
  {% with comments.count as total_comments %}
    <h2>
      {{ total_comments }} comment{{ total_comments|pluralize }}
    </h2>
  {% endwith %}
{% endblock %}
```
### blog/post/detail.html
>
```
{% extends "blog/base.html" %}
{% block title %}{{ post.title }}{% endblock %}
{% block content %}
  <h1>{{ post.title }}</h1>
  <p class="date">
    Published {{ post.publish }} by {{ post.author }}
  </p>
  {{ post.body|linebreaks }}
  <p>
    <a href="{% url "blog:post_share" post.id %}">
      Share this post
    </a>
  </p>
  {% with comments.count as total_comments %}
    <h2>
      {{ total_comments }} comment{{ total_comments|pluralize }}
    </h2>
  {% endwith %}
  {% for comment in comments %}
    <div class="comment">
      <p class="info">
        Comment {{ forloop.counter }} by {{ comment.name }}
        {{ comment.created }}
      </p>
      {{ comment.body|linebreaks }}
    </div>
  {% empty %}
    <p>There are no comments.</p>
  {% endfor %}
{% endblock %}
```

### blog/post/detail.html 
>
```
{% extends "blog/base.html" %}
{% block title %}{{ post.title }}{% endblock %}
{% block content %}
  <h1>{{ post.title }}</h1>
  <p class="date">
    Published {{ post.publish }} by {{ post.author }}
  </p>
  {{ post.body|linebreaks }}
  <p>
    <a href="{% url "blog:post_share" post.id %}">
      Share this post
    </a>
  </p>
  {% with comments.count as total_comments %}
    <h2>
      {{ total_comments }} comment{{ total_comments|pluralize }}
    </h2>
  {% endwith %}
  {% for comment in comments %}
    <div class="comment">
      <p class="info">
        Comment {{ forloop.counter }} by {{ comment.name }}
        {{ comment.created }}
      </p>
      {{ comment.body|linebreaks }}
    </div>
  {% empty %}
    <p>There are no comments.</p>
  {% endfor %}
  {% include "blog/post/includes/comment_form.html" %}
{% endblock %}
```

### 
>
```

```

### 
>
```

```

### 
>
```

```

### 
>
```

```

### 
>
```

```

### 
>
```

```


### 
>
```

```

