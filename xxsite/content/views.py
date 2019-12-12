import redis

from datetime import date

from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.cache import cache
from django.http import HttpResponse

from .models import (
    Article, IndexContent, Category,
    Tag, Page, SideBar, Link,
)
from xxsite.settings import SITE_URL, SITE_NAME, SITE_DESCRIPTION, BEIAN

# Create your views here.
class GenericViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all(),
            'sidebars': SideBar.objects.all(),
            'pages': Page.objects.filter(does_nav=True),
            'links': Link.objects.all(),
            'site_url': SITE_URL,
            'site_name': SITE_NAME,
            'site_description': SITE_DESCRIPTION,
            'beian': BEIAN,
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

        pv_key = 'pv:' + self.request.path
        rd = redis.Redis(host='localhost', port=6379, db=0)
        if rd.exists(pv_key):
            pv = str(rd.get(pv_key), encoding='utf-8')
        else:
            pv = 1
        article_id = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=article_id)
        context.update({
            'article': article,
            'tags': article.tag.all(),
            'pv': pv,
        })
        return context


class CategoryView(GenericViewMixin, ListView):
    queryset = Article.objects.all()
    template_name = "content/category.html"
    context_object_name = "articles"
    paginate_by = 8

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
    paginate_by = 8

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

def stat(request):
    """
    暂时用于 web 端查看访问数据
    """
    import time
    time.sleep(3)
    rd = redis.Redis(host='localhost', port=6379, db=0)
    today_str = str(date.today())
    uv_key_day = 'uv:' + today_str
    uv_key_all = 'uv_all'
    pv_key_day = 'pv:' + today_str
    pv_key_all = 'pv_all'

    if rd.exists(uv_key_day):
        uv_day = str(rd.get(uv_key_day), encoding='utf-8')
    else:
        uv_day = 0

    if rd.exists(uv_key_all):
        uv_all = str(rd.get(uv_key_all), encoding='utf-8')
    else:
        uv_all = 0

    if rd.exists(pv_key_day):
        pv_day = str(rd.get(pv_key_day), encoding='utf-8')
    else:
        pv_day = 0

    if rd.exists(uv_key_all):
        pv_all = str(rd.get(pv_key_all), encoding='utf-8')
    else:
        pv_all = 0

    html = "<p>日期：%s</p><p>PV(今日/总)：%s/%s</p><p>UV(今日/总)：%s/%s</p>" % (
        today_str, pv_day, pv_all, uv_day, uv_all)
    return HttpResponse(html)
