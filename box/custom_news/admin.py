# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.urls import reverse
from django.http import HttpResponseRedirect
from easy_news.admin import NewsAdmin
from easy_news.models import News
from box.links.admin import LinkInline
from box.gallery.admin import HeroInline
from .forms import NewsRootAdminForm
from .models import NewsRoot


@admin.register(NewsRoot)
class NewsRootAdmin(admin.ModelAdmin):

    @property
    def media(self):
        media = super(NewsRootAdmin, self).media
        media.add_css({'all': ['css/admin/common.css']})
        return media

    model = NewsRoot
    form = NewsRootAdminForm
    inlines = [HeroInline, LinkInline]

    def has_add_permission(self, request):
        return not bool(NewsRoot.objects.exists())

    def has_delete_permission(self, request, obj=None):
        return False

    def response_post_save_change(self, request, obj):

        """ Редирект на страницу списка новостей после сохранения """

        post_url = reverse('admin:easy_news_news_changelist', current_app=self.admin_site.name)
        return HttpResponseRedirect(post_url)


class CustomNewsAdmin(NewsAdmin):

    inlines = [HeroInline, LinkInline]

try:
    admin.site.unregister(News)
    admin.site.register(News, CustomNewsAdmin)
except NotRegistered:
    pass
