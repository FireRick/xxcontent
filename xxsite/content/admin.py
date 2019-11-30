from django.contrib import admin

from .adminforms import DescAdminForm
from .models import (
    Category, Tag, Article,
    SideBar, IndexContent, Page, Link
)

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    form = DescAdminForm


class TagAdmin(admin.ModelAdmin):
    form = DescAdminForm


class ArticleAdmin(admin.ModelAdmin):
    form = DescAdminForm
    fieldsets = [
        ('文章元数据', {'fields': [
            'title', 'author', 'create_time',
            'update_time', 'category', 'tag',
        ]}),
        ('摘要和正文', {'fields': [
            'desc', 'content',
        ]}),
    ]
    list_display = ('title', 'author', 'create_time', 'category')
    list_filter = ['category']


class SideBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'sidebar_type', 'order_number')


class IndexContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'order_number')


class PageAdmin(admin.ModelAdmin):
    form = DescAdminForm
    fieldsets = [
        ('页面元数据', {'fields': [
            'link_word', 'title', 'author', 'create_time',
            'update_time', 'does_follow', 'does_nav',
        ]}),
        ('摘要和正文', {'fields': [
            'desc', 'content',
        ]}),
    ]
    list_display = ('title', 'author', 'create_time', 'does_nav')
    list_filter = ['does_follow']


class LinkAdmin(admin.ModelAdmin):
    list_display = ('anchor_word', 'create_time', 'does_follow', 'order_number')
    list_filter = ['does_follow']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(SideBar, SideBarAdmin)
admin.site.register(IndexContent, IndexContentAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Link, LinkAdmin)
