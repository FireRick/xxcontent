from django.shortcuts import render, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import (
    Article, IndexContent, Category,
    Tag, Page,
)

# Create your views here.
class IndexView(TemplateView):
    template_name = "content/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_blocks'] = IndexContent.get_all()
        return context


class ArticleView(DetailView):
    model = Article
    template_name = "content/article.html"
    context_object_name = "article"

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class CategoryView(ListView):
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


class TagView(ListView):
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

class PageView(DetailView):
    model = Page
    template_name = "content/page.html"
    pk_url_kwarg = "link_word"
    context_object_name = "page"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
