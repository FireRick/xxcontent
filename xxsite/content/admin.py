from django.contrib import admin

from .models import (
    Category, Tag, Article,
    SideBar, Page, Link
)

# Register your models here.
class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ('文章元数据', {'fields': [
            'title', 'author', 'create_time',
            'update_time', 'category', 'tag',
        ]}),
        ('摘要和正文', {'fields': [
            'desc', 'content',
        ]}),
    ]
    list_display = ('title', 'author', 'create_time', 'category', 'pv', 'uv')
    list_filter = ['category']


class SideBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'sidebar_type')


class PageAdmin(admin.ModelAdmin):
    fieldsets = [
        ('页面元数据', {'fields': [
            'url', 'title', 'author',
            'create_time', 'update_time', 'does_follow',
        ]}),
        ('摘要和正文', {'fields': [
            'desc', 'content',
        ]}),
    ]
    list_display = ('title', 'author', 'create_time', 'does_follow', 'pv', 'uv')
    list_filter = ['does_follow']


class LinkAdmin(admin.ModelAdmin):
    list_display = ('anchor_word', 'create_time', 'does_follow')
    list_filter = ['does_follow']


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Article, ArticleAdmin)
admin.site.register(SideBar, SideBarAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Link, LinkAdmin)