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
from django.urls import path
from django.contrib.sitemaps.views import sitemap

from content.views import (
    IndexView, ArticleView, CategoryView,
    TagView, PageView, ArticleSitemap,
    PageSitemap, CategorySitemap,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('category/<int:cat_id>/', CategoryView.as_view(), name='category'),
    path('tag/<int:tag_id>/', TagView.as_view(), name='tag'),
    path('<link_word>/', PageView.as_view(), name='page'),
    path('article/<pk>/', ArticleView.as_view(), name='article'),
    path(
        'sitemap.xml', sitemap, {
        'sitemaps': {
            'articles': ArticleSitemap,
            'page': PageSitemap,
            'category': CategorySitemap,
            },
        'template_name': 'content/sitemap.xml',
        },
        name='django.contrib.sitemaps.views.sitemap'
    ),
]
