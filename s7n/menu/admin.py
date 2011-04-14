from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from s7n.menu.models import Menu

admin.site.register(Menu, MPTTModelAdmin)