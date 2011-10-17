from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from samklang_menu.models import Menu

admin.site.register(Menu, MPTTModelAdmin)
