from django.conf.urls import *
from samklang_menu.views import list_menu, new_menuitem, delete_menuitem

urlpatterns = patterns('',
    (r'^$', list_menu, {}, 'menu-list'),
    (r'^new/$', new_menuitem, {}, 'menu-new'),
    (r'^delete/$', delete_menuitem, {}, 'menu-delete'),
)
