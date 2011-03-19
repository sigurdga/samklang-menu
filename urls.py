from django.conf.urls.defaults import *
from strekmann_menu.views import list_menu, new_menuitem

urlpatterns = patterns('',
    (r'^list/(?P<id>\d+)$', list_menu, {}, 'strekmann_menu_list'),
    (r'^new/(?P<tree_id>\d+)$', new_menuitem, {}, 'strekmann_menu_new'),
)
