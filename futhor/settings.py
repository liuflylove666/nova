    # -*- coding:utf-8 -*-
"""
Django settings for futhor project.

Generated by 'django-admin startproject' using Django 1.10.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""
from __future__ import absolute_import
import os
import configmodule
config_mode = configmodule.config_mode
if config_mode == 'Development':
    Configs = configmodule.DevelopmentConfig
if config_mode == 'Testing':
    Configs = configmodule.TestingConfig
if config_mode == 'Production':
    Configs = configmodule.ProductionConfig

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&%6a=aw^a_0)@-ob9)2=bb9dwt!qa!$7dege=y0!jype9&_v70'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = Configs.DEBUG

# ALLOWED_HOSTS = ['127.0.0.1']
ALLOWED_HOSTS = Configs.ALLOWED_HOSTS

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'nova',
    'djcelery',
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

ROOT_URLCONF = 'futhor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'futhor.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'dev',
#         'USER': 'dev',
#         'PASSWORD': 'dev',
#         'HOST': '10.126.3.13',
#         'PORT': '3306',
#     }
# }
DATABASES = Configs.DATABASES

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = '/nova/login/'

# session 8小时过期
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 60 * 60 * 8
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

import djcelery
from celery.schedules import crontab
djcelery.setup_loader()
from datetime import timedelta
# config Broker
# BROKER_URL = 'redis://10.126.3.13:6379/0'
BROKER_URL = Configs.BROKER_URL
# BROKER_TRANSPORT = 'redis'
BROKER_TRANSPORT = Configs.BROKER_TRANSPORT

# CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
# CELERY_RESULT_BACKEND = 'redis://10.126.3.13:6379/2'
CELERY_RESULT_BACKEND = Configs.CELERY_RESULT_BACKEND
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'

# 每个worker执行了多少任务就会死掉
CELERY_MAX_TASKS_PER_CHILD = 100
# 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}

CELERYBEAT_SCHEDULE = {
    'update-task-status-every-60s': {
        'task': 'nova.tasks.update_task_status',
        'schedule': timedelta(seconds=60),
        # 'args': (16, 17)
    },
    'http-test-every-60s': {
        'task': 'nova.tasks.get_http_mon_data',
        'schedule': timedelta(seconds=60),
    },
    'query-fpcy-every-day': {
        'task': 'nova.tasks.query_fpcy_every_day',
        'schedule': crontab(minute=1, hour=22),
    },
    'http-test-every-60s': {
        'task': 'nova.tasks.get_service_mon_data',
        'schedule': timedelta(seconds=60),
     },
}

# 2017-10-19:
LOGTAIL_FILES = {
    'django': os.path.join(BASE_DIR, 'nova.log')
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        # 针对 DEBUG = True 的情况
    },
    'formatters': {
        'standard': {
            # 对日志信息进行格式化，每个字段对应了日志格式中的一个字段，输出类似于下面的内容
            # 'format': '''%(levelname)s "%(asctime)s" "%(pathname)s" "%(filename)s" "%(module)s" "%(funcName)s" "%(lineno)d": "%(message)s"'''
            'format': '''%(asctime)s %(levelname)s "%(module)s.%(funcName)s" "%(lineno)d": "%(message)s"'''
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'standard'
        },
        'file_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', Configs.LOG_FILE_NAME),
            'formatter': 'standard'
        },  # 用于文件输出
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file_handler', 'console'],
            'level': 'DEBUG',
            'propagate': True  # 是否继承父类的log信息
        },  # handlers 来自于上面的 handlers 定义的内容
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
