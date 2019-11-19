from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers

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


@method_decorator(vary_on_headers('User-Agent'), name='dispatch')
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
