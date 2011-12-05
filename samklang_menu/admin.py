from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from samklang_menu.models import Menu, Widget


class WidgetInline(admin.TabularInline):
    model = Widget


class MenuAdmin(MPTTModelAdmin):
    inlines = [ WidgetInline ]

admin.site.register(Menu, MenuAdmin)
