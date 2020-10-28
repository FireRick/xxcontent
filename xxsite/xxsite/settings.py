import os


VERSION = '${version}'


DEBUG = True


# 解析 ~/.xxsite/xxsite.conf 中的站点信息
conf_file = os.path.join(os.environ['HOME'], '.xxsite/xxsite.conf')
conf = {}
with open(conf_file, 'r') as f:
    for line in f:
        line = line.strip()
        # if line is not blank or comment, enter
        if line and line[0] != '#':
                split_res = line.split('=')
                if len(split_res) == 2:
                    conf[split_res[0].strip()] = split_res[1].strip()
    if len(conf) != 7:
        raise ValueError("Invalid format in xxsite.conf.")

# get information about site
SITE_DOMAIN = conf['SITE_DOMAIN']
SITE_URL = 'http://' + SITE_DOMAIN
SITE_NAME = conf['SITE_NAME']
SITE_DESCRIPTION = conf['SITE_DESCRIPTION']
BEIAN = conf['BEIAN']
CDN = conf['CDN']


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


SECRET_KEY = conf['SECRET_KEY']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'xxcontent',
        'USER': 'fire',
        'PASSWORD': conf['DB_PASSWORD'],
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'CONN_MAX_AGE': 5 * 60,
        'OPTIONS': {'charset': 'utf8'},
        'TEST': {
            'CHARSET': 'utf8',
        }
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'TIMEOUT': 30,
        # 'KEY_FUNCTION': 'content.cache.make_key',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        },
        'CONNECTION_POOL_CLASS': 'redis.connection.BlockingConnectionPool',
    }
}


INSTALLED_APPS = [
    'content',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    # 'content.middleware.uid.UidMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'content.middleware.uid.UidMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'xxsite.urls'

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

WSGI_APPLICATION = 'xxsite.wsgi.application'


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

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_ROOT = os.path.dirname(BASE_DIR) + '/static_files/'


if DEBUG:
    ALLOWED_HOSTS = ['*']

    INSTALLED_APPS += [
        'debug_toolbar',
        # 'silk',
        'pympler',
        # 'debug_toolbar_line_profiler',
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        # 'silk.middleware.SilkyMiddleware',
    ]

    INTERNAL_IPS = ['127.0.0.1', '192.168.88.1']

    DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': 'https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js',
    }

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
        'pympler.panels.MemoryPanel',
        # 'djdt_flamegraph.FlamegraphPanel',
    #    'debug_toolbar_line_profiler.panel.ProfilingPanel',
    ]

    STATIC_URL = '/static/'
    SITE_URL = '' # 调试模式中用相对路径替代

else:
    ALLOWED_HOSTS = [SITE_DOMAIN, '127.0.0.1']

    if CDN:
        STATIC_URL = CDN + '/static/'  # cdn
    else:
        STATIC_URL = '/static/'

