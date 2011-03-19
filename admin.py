from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from strekmann_menu.models import Menu

admin.site.register(Menu, MPTTModelAdmin)