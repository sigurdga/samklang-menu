from django.conf.urls.defaults import *
from samklang_menu.views import list_menu, new_menuitem, delete_menuitem

urlpatterns = patterns('',
    (r'^list/(?P<tree_id>\d+)$', list_menu, {}, 'strekmann_menu_list'),
    (r'^new/(?P<tree_id>\d+)$', new_menuitem, {}, 'strekmann_menu_new'),
    (r'^delete/(?P<tree_id>\d+)$', delete_menuitem, {}, 'strekmann_menu_delete'),
)
