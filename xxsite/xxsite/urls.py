"""xxsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.contrib.sitemaps.views import sitemap

from content.views import (
    IndexView, ArticleView, CategoryView,
    TagView, PageView,
)
from content.sitemap import (
    ArticleSitemap, PageSitemap, CategorySitemap,
    IndexSitemap, TagSitemap,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', cache_page(1200)(IndexView.as_view()), name='index'),
    path('category/<int:cat_id>/', cache_page(1200)(CategoryView.as_view()), name='category'),
    path('tag/<int:tag_id>/', cache_page(1200)(TagView.as_view()), name='tag'),
    path('<link_word>/', cache_page(1200)(PageView.as_view()), name='page'),
    path('article/<pk>/', cache_page(1200)(ArticleView.as_view()), name='article'),
    path(
        'sitemap.xml', cache_page(1200)(sitemap), {
        'sitemaps': {
            'index': IndexSitemap,
            'category': CategorySitemap,
            'tag': TagSitemap,
            'articles': ArticleSitemap,
            'page': PageSitemap,
            },
        'template_name': 'content/sitemap.xml',
        },
        name='django.contrib.sitemaps.views.sitemap'
    ),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        # path('silk/', include('silk.urls', namespace='silk')),
    ]
