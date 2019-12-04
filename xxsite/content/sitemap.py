from django.contrib.sitemaps import Sitemap
from django.urls import reverse
# from django.contrib.sitemaps.views import sitemap
# from django.core.cache import cache

from .models import Article, Category, Tag, Page


class ArticleSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.update_time

    def location(self, obj):
        return reverse('article', args=[obj.pk])


class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Page.objects.all()

    def lastmod(self, obj):
        return obj.update_time

    def location(self, obj):
        return reverse('page', args=[obj.pk])


class CategorySitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        return Article.objects.order_by('-update_time')[0].update_time

    def location(self, obj):
        return reverse('category', args=[obj.pk])


class TagSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Tag.objects.all()

    def lastmod(self, obj):
        return Article.objects.order_by('-update_time')[0].update_time

    def location(self, obj):
        return reverse('tag', args=[obj.pk])


class IndexSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return ['index']  # 只要是一个 len=1 的列表即可，与内容无关

    def lastmod(self, obj):
        return Article.objects.order_by('-update_time')[0].update_time

    def location(self, obj):
        return reverse('index')
