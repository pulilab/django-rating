This package allows you to rate any of your objects with different type of ratings.

Example:

Let's say a user (as a participant) wants to rate the last session's content and the performer.

```python
rating_element_1 = RatingElement.objects.create(element_type=RATING_ELEMENT_SESSION_CONTENT, score=5)
rating_element_2 = RatingElement.objects.create(element_type=RATING_ELEMENT_SESSION_PERFORMER, score=5)

rating = ObjectRating.objects.create(
    user=my_user,
    user_type=USER_TYPE_PARTICIPANT,
    content_type=ContentType.objects.get(model="session"),
    object_id=Session.objects.last().id, 
)

rating.elements.add(rating_element_1, rating_element_2)
```

# Installation

Install the pip package:

```bash
pip install django-rating
```

Install `django-rest-framework` if not already installed

add `rating` and `rest_framework` to INSTALLED_APPS

include 'rating.urls' into urlpatterns

```python
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"", include("rating.urls")),
]
```

Migrate the db to crate rating models

```bash
python manage.py migrate
```

# Develop

Clone the repo

```bash
git clone git@github.com:pulilab/django-rating.git
```

## Test app

Test standalone app:

$ export DATABASE_URL='your_db'  # you can skip this, defaults to 'localhost' (use postgres.app for simplicity)

$ pip install -r requirements.txt

$ python runtests.py

## Run the app in develop mode

Create a new django project and install the package in develop mode

```bash
django-admin startproject rating_demo
cd rating_demo
pip install -e ~LOCAL_PATH_TO_DJANGO_RATING
```

Add `rating` and `rest_framework` to `INSTALLED_APPS` in `settings.py`

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rating'
]
```
Configure demo app urls

```python
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"^api/", include("rating.urls")),
]
```
> SqlLite is not supported

Change the db config to use postgres in `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': os.environ.get("DATABASE_URL", 'localhost'),
        'PORT': 5432,
    }
}
```

# Configure

Configure the following values in settings:
- RATING_VALID_USER_TYPES: Defines the accepted user types
- RATING_VALID_ELEMENT_TYPES: Defines the accepted rating element types
- RATING_MIN_SCORE: Defines the minimum score for rating
- RATING_MAX_SCORE: Defines the maximum score for rating

E.g.
```python
from django.utils.translation import ugettext_lazy as _

USER_TYPE_SESSION_HOST = 'H'
USER_TYPE_SESSION_PARTICIPANT = 'P'

ELEMENT_TYPE_SESSION_CONTENT = 'S'
ELEMENT_TYPE_COMMENT = 'C'

RATING_VALID_USER_TYPES = (
    (USER_TYPE_SESSION_HOST, _('HOST')),
    (USER_TYPE_SESSION_PARTICIPANT, _('PARTICIPANT'))
)
RATING_VALID_ELEMENT_TYPES = (
    (ELEMENT_TYPE_SESSION_CONTENT, _('SESSION_CONTENT')),
    (ELEMENT_TYPE_COMMENT, _('COMMENT'))
)
RATING_MIN_SCORE = 1
RATING_MAX_SCORE = 5

```


Migrate db, create super user and run your demo app:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

open the browser at `http://localhost:8000/admin`

