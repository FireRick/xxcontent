from django.shortcuts import render
from django.views.generic.base import TemplateView

from .models import (
    Article, IndexContent,
)

# Create your views here.
class IndexView(TemplateView):
    template_name = "content/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['content_blocks'] = IndexContent.get_all()
        return context
