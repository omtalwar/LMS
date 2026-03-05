from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


# 🔐 SECURITY
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")

# ❌ NEVER keep DEBUG True in production
DEBUG = os.getenv("DEBUG", "False") == "True"
# DEBUG = True

# 🔥 Railway / production hosts
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")


# 🔥 APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'courses',
]


# 🔥 MIDDLEWARE (WhiteNoise enabled)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # WhiteNoise MUST be right after SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    # Optional but recommended later (CSRF secure for prod)
    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'lms_project.urls'


# 🔥 TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # safer absolute path
        'DIRS': [BASE_DIR / "templates"],

        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'lms_project.wsgi.application'


# 🔥 DATABASE
# Railway can override this later if you add PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# 🔐 PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# 🌍 INTERNATIONAL
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# 🔥 STATIC FILES (PRODUCTION SAFE)
STATIC_URL = '/static/'

# where collectstatic will dump files
STATIC_ROOT = BASE_DIR / 'staticfiles'

# keep empty unless you have a local static folder
STATICFILES_DIRS = []

# WhiteNoise optimized static serving
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# 🔥 DEFAULT PRIMARY KEY
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'