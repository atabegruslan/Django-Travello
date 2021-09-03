# Django Travello

## Tutorials

- Preliminaries: https://github.com/Ruslan-Aliyev/Python_Django_Tutorial
- Django REST API: https://www.youtube.com/playlist?list=PLgCYzUzKIBE9Pi8wtx8g55fExDAPXBsbV
	- https://www.django-rest-framework.org/tutorial/quickstart/

## Related Projects

A similar but older and simpler project: https://github.com/Ruslan-Aliyev/Django-MVC

# Let's start

```
django-admin startproject travello 
cd travello
python manage.py startapp frontend     
```

1. Use existing template: https://colorlib.com/wp/template/travello/

2. Copy the downloaded Travello's `index.html` into `templates/` as `frontend.html`

3. `travello/urls.py`
```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('travello', include('frontend.urls')),
]
```

4. `frontend/urls.py`
```py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

5. `frontend/views.py`
```py
from django.shortcuts import render

def index(request):
	return render(request, "frontend.html")
```

6. `travello/settings.py`
```py
import os
...
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
```

7. Launch server to see: `python manage.py runserver`

But now all the media links are wrong.

### Static files

6. Create a 'static' folder. Copy all the css, js and images into it.

7. Add to `travello/settings.py`
```py
# ...
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
```

8. Then run `python manage.py collectstatic`, an 'assets' folder will be there.

9. Now in `frontend.html`, change things like `href="styles/bootstrap4/bootstrap.min.css"` to `href="{% static 'styles/bootstrap4/bootstrap.min.css' %}"`

10. Tell Django to load static files first by putting `{% load static %}` at the top of `frontend.html`.

### Send data to the template

11. `frontend/models.py`
```py
from django.db import models

class Destination:
	id    : int
	name  : str
	img   : str
	desc  : str
	price : int
	offer : bool
```

12. `frontend/views.py`
```py
from django.shortcuts import render
from .models import Destination

def index(request):
	dest1 = Destination()
	dest1.name = 'Mumbai'
	dest1.desc = 'Beautiful City'
	dest1.img = 'destination_3.jpg'
	dest1.price = 700
	dest1.offer = True

	dest2 = Destination()
	dest2.name = 'Mumbai'
	dest2.desc = 'Beautiful City'
	dest2.img = 'destination_3.jpg'
	dest2.price = 700
	dest2.offer = False

	dests = [dest1,dest2]
	
	return render(request, "frontend.html", {'dests': dests})
```

13. `templates/frontend.html`
```html
{% load static %}
{% static "images" as baseUrl %} <!-- Add this line -->

<!-- ... -->

<!-- Alter Destination section as below -->
{% for dest in dests %}
<!-- Destination -->
<div class="destination item">
	<div class="destination_image">
		<img src="{{baseUrl}}/{{dest.img}}" alt="">
		{% if dest.offer %}
		<div class="spec_offer text-center"><a href="#">Special Offer</a></div>
		{% endif %}
	</div>
	<div class="destination_content">
		<div class="destination_title"><a href="destinations.html">{{dest.name}}</a></div>
		<div class="destination_subtitle"><p>{{dest.desc}}</p></div>
		<div class="destination_price">From ${{dest.price}}</div>
	</div>
</div>
{% endfor %}
```

## Adding DB

1. Download and install:

![](/Illustrations/postgresql.PNG)

2. Install DB adapter: `pip install psycopg2` 

3. `travello/settings.py`
```py
INSTALLED_APPS = [
    'frontend.apps.FrontendConfig', # Name of app + 'Config'
    # ...
]

# ...

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travello',
        'USER': 'postgres',
        'PASSWORD': '***', # Your PostgreSql DB password
        'HOST': 'localhost',
    }
}
```

Now make that database

4. Alter `frontend/models.py` to
```py
class Destination(models.Model):
	#id: int
	name  = models.CharField(max_length=100)
	img   = models.ImageField(upload_to='pics')
	desc  = models.TextField()
	price = models.IntegerField()
	offer = models.BooleanField(default=False)
```

Refer to: https://docs.djangoproject.com/en/3.1/ref/models/fields/

5. When using ImageField, need to `pip install Pillow`

6. `python manage.py makemigrations` - new migration file is created in `frontend/migrations/` .

7. `python manage.py sqlmigrate frontend 0001` - will let you see the SQL code that would execute.

8. `python manage.py migrate` - actually migrates. You'll see the results in the DB. PgAdmin: Servers -> PostgreSQL -> Databases -> travello -> schemas -> public -> Tables.

### Back Office

We want to insert new entries via the backend.

Django gives an inbuilt admin backside: http://localhost:8000/admin

9. But need to create super-admin by: `python manage.py createsuperuser`

10. `frontend/admin.py`
```py
from django.contrib import admin
from .models import Destination

admin.site.register(Destination)
```

![](/Illustrations/backoffice.PNG)

11. Add to `travello/settings.py`
```py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

12. Edit `travello/urls.py`
```py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings            # Add this
from django.conf.urls.static import static  # Add this

urlpatterns = [
    path('admin/', admin.site.urls),
    path('travello', include('frontend.urls')),
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Add this
```

13. Add some entries via the backend

Note: Recall `pics` folder from step 4. Uploaded images will end up in `media/pics/`.

14. Edit `frontend/views.py`
```py
def index(request):
	dests = Destination.objects.all()
	return render(request, "frontend.html", {'dests': dests})
```

15. But now the image links are out of place. 

So now in `templates/frontend.html`, replace `<img src="{{baseUrl}}/{{dest.img}}" alt="">` with `<img src="{{dest.img.url}}" alt="">`

## User accounts

1. `python manage.py startapp accounts`

2. `accounts/urls.py`
```py
from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]
```

3. Do `accounts/views.py` 

4. Add `templates/register.html` & `templates/login.html`

We are utilizing the inbuilt `auth_user` table, so make the registration form fields accordingly.

5. Add `path('accounts/', include('accounts.urls'))` to `travello/urls.py`

6. Add to `templates/frontend.html`
```html
{% if user.is_authenticated %}
<li>Hello, {{user.first_name}}</li>
<li><a href="accounts/logout">Logout</a></li>
{% else %}
<li><a href="accounts/register">Register</a></li>
<li><a href="accounts/login">Login</a></li>
{% endif %}
```

# RESTful API

Intention is to add API to the `travello` app.

1. `pip install djangorestframework`

2. `travello/settings.py`
```py
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

3. `travello/urls.py`
```py
# ...
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('calc.urls')),
    path('travello', include('frontend.urls')),
    path('accounts/', include('accounts.urls')),
    
    # REST
    path('api/travello', include('frontend.api.urls', 'travello_api')), # Add this
]
```

4. Create `frontend/api/serializers.py`
```py
from rest_framework import serializers
from frontend.models import Destination

class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ['id', 'name', 'img', 'desc', 'price', 'offer']
```

NOTE: Don't forget to put `__init__.py` into `api` folder when you create the `api` folder.

5. `frontend/api/urls.py`

Just do the GETs for now:

```py
from django.urls import path
from frontend.api.views import (api_index, api_dest)

app_name = 'travello'

urlpatterns = [
    path('/', api_index, name='index'),
    path('/<id>/', api_dest, name='dest'),
]
```

6. `frontend/api/views.py`
```py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from frontend.models import Destination
from frontend.api.serializers import DestinationSerializer

@api_view(['GET'])
def api_index(request):
	dests = Destination.objects.all()
	serializer = DestinationSerializer(dests, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def api_dest(request, id):

	try:
		dest = Destination.objects.get(id=id)
	except Destination.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	serializer = DestinationSerializer(dest)
	return Response(serializer.data)
```

7. See from browser: `http://localhost:8000/api/travello/` & `http://localhost:8000/api/travello/1/`

8. Finish the rest of the CRUD. See `travello/api/urls.py` & `travello/api/views.py`

Try POST from Postman:

![](/Illustrations/api_post.PNG)

## User accounts via API

1. Do `accounts/models.py`

2. Complete all inside `accounts/api/`

3. `travello/urls.py`
```py
# ...
urlpatterns = [
    # REST
    path('api/travello', include('frontend.api.urls', 'travello_api')),
    path('api/accounts', include('accounts.api.urls', 'accounts_api')), # Add this
]
```

4. `travello/settings.py`
```py
INSTALLED_APPS = [
    'accounts',  # Add this
    'frontend.apps.FrontendConfig',
    'django.contrib.admin',
    #...
    'rest_framework',
    'rest_framework.authtoken',  # Add this
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',  # Add these
    ]
}
```

5. Run `python manage.py migrate` to create `authtoken_token` table.

6. Now you can try Register and Login

```
curl --location --request POST 'http://127.0.0.1:8000/api/accounts/register' \
--form 'email="test@user.com"' \
--form 'username="testuser"' \
--form 'password="Abcdefg8!"' \
--form 'password2="Abcdefg8!"' \
--form 'first_name="Test"' \
--form 'last_name="User"'
```

```
curl --location --request POST 'http://127.0.0.1:8000/api/accounts/login' \
--form 'email="test@user.com"' \
--form 'username="testuser"' \
--form 'password="Abcdefg8!"'
```
