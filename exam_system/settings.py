from pathlib import Path
import os
from dotenv import load_dotenv
from permit import Permit  # We can keep this since it's being used

# Load environment variables
load_dotenv()

# Load the secret key from .env or use the fallback
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'gtiwjg^_67co3ubz#^yruiuh3z&3f)=m$36)=zw-)h(*j(f=o@')

# Debugging log for Permit API key (optional)
print("PERMIT_API_KEY from .env:", os.getenv("PERMIT_API_KEY"))

# Set up Permit-related environment variables
PERMIT_API_KEY = os.getenv("PERMIT_API_KEY", "")
PERMIT_PDP_URL = os.getenv("PERMIT_PDP_URL", "https://cloudpdp.api.permit.io")  # or whatever PDP you're using

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Django Debugging settings
DEBUG = True  # Set to False later when deploying

# Allowed hosts settings
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Required if DEBUG is False

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'exam_system'),
        'USER': os.getenv('DB_USER', 'exam_user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'your_secure_password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'permit',
    'accounts',  # App to manage user accounts
    'exams',     # App for exams management
    'results',   # App for results
]

ROOT_URLCONF = 'exam_system.urls'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Configure REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.ExamPermitMiddleware',  # Only if you're using Permit middleware
]

# Redirect URL after successful login
LOGIN_REDIRECT_URL = '/'

# Static files configuration
STATIC_URL = '/static/'

# Database backup options, this may be needed in the future
DATABASE_ROUTERS = []

# Time zone and locale settings
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static file configuration (optional)
STATICFILES_DIRS = []
