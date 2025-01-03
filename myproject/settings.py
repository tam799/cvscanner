# ...existing code...
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# ...existing code...

SECRET_KEY = 'x-g^xu0^9=1gdr2#-lv$ju(ui&()n^0(@*mk^4h9w&beljv#$*'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cvapp',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# ...existing code...

ROOT_URLCONF = 'myproject.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'local instance MySQL80',  # Replace with your actual database name
        'USER': 'user',  # Replace with your actual database user
        'PASSWORD': 'Abcdefghijk1',  # Replace with your actual database password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
]

WSGI_APPLICATION = 'myproject.wsgi.application'

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]  # Ensure this is the correct path to your CSS files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# File storage settings
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


LOGOUT_REDIRECT_URL = 'cvapp:home'

# ...existing code...
