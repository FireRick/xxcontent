from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import (
    Article, IndexContent, Category,
    Tag, Page, SideBar, Link,
)

# Create your views here.
class GenericViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all(),
            'sidebars': SideBar.objects.all(),
            'pages': Page.objects.filter(does_nav=True),
            'links': Link.objects.all(),
        })
        return context


class IndexView(GenericViewMixin, TemplateView):
    template_name = "content/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_blocks'] = IndexContent.get_all()
        return context


class ArticleView(GenericViewMixin, TemplateView):
    # queryset = Article.objects.all()
    template_name = "content/article.html"
    # context_object_name = "article"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article_id = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_id)
        context.update({
            'article': article,
            'tags': article.tag.all(),
        })
        return context


class CategoryView(GenericViewMixin, ListView):
    queryset = Article.objects.all()
    template_name = "content/category.html"
    context_object_name = "articles"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_id = self.kwargs.get('cat_id')
        category = get_object_or_404(Category, pk=cat_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        cat_id = self.kwargs.get('cat_id')
        return queryset.filter(category_id=cat_id)


class TagView(GenericViewMixin, ListView):
    queryset = Article.objects.all()
    template_name = "content/tag.html"
    context_object_name = "articles"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)

class PageView(GenericViewMixin, DetailView):
    model = Page
    template_name = "content/page.html"
    pk_url_kwarg = "link_word"
    context_object_name = "page"


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
        return obj.update_time

    def location(self, obj):
        return reverse('category', args=[obj.pk])


class TagSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return Tag.objects.all()

    def lastmod(self, obj):
        return obj.update_time

    def location(self, obj):
        return reverse('tag', args=[obj.pk])


class IndexSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return [Article.objects.order_by('-update_time')[0]]  # 中括号包裹，形成序列，否则 len() 调用会出错

    def lastmod(self, obj):
        return obj.update_time

    def location(self, obj):
        return reverse('index')
