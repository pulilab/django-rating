import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner
from django.core.management import call_command


if __name__ == "__main__":
    DIRNAME = os.path.dirname(__file__)
    settings.configure(
        DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'postgres',
                'USER': 'postgres',
                'HOST': os.environ.get("DATABASE_URL", 'localhost'),
                'PORT': 5432,
            }
        },
        MIDDLEWARE=[
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ],
        EMAIL_BACKEND='django.core.mail.backends.dummy.EmailBackend',
        ROOT_URLCONF='rating.urls',
        INSTALLED_APPS=('django.contrib.auth',
                        'django.contrib.contenttypes',
                        'django.contrib.sessions',
                        'django.contrib.admin',
                        'rating'),
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': ['templates'],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
                },
            },
        ],
    )

    django.setup()
    call_command('makemigrations', 'rating')
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['rating'])
    sys.exit(bool(failures))
