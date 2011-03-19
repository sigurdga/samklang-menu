from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.utils import simplejson
from django.db import connection, transaction

from strekmann_menu.models import Menu
from strekmann_menu.forms import MenuForm

def list_menu(request, id):
    if request.method == 'POST':
        id = request.POST["id"]
        menu = get_object_or_404(Menu, pk=id)
        try:
            # get tree from json-data
            tree = simplejson.loads(request.POST["mptt_tree"])
            
            # format tree, remove root-item and make root-parents = id
            for node in tree:
                if node['parent_id'] == 'root':
                    node['parent_id'] = id
                if node['item_id'] == 'root':
                    tree.remove(node)
            
            tree_id = menu.tree_id
            cursor = connection.cursor()
            qn = connection.ops.quote_name
            opts = menu._meta
        
            cursor.executemany("""
                UPDATE %(table)s 
                SET %(parent)s = :parent_id,
                    %(left)s = :left,
                    %(right)s = :right,
                    %(level)s = :depth 
                WHERE %(pk)s = :item_id AND %(tree_id)s = %(given_tree_id)s""" % {
                    "table": qn(opts.db_table),
                    'level': qn(opts.get_field(opts.level_attr).column),
                    'left': qn(opts.get_field(opts.left_attr).column),
                    'tree_id': qn(opts.get_field(opts.tree_id_attr).column),
                    'right': qn(opts.get_field(opts.right_attr).column),
                    'parent': qn(opts.get_field(opts.parent_attr).column),
                    'pk': qn(opts.pk.column),
                    'given_tree_id': tree_id,
                }, tree)
            transaction.commit_unless_managed()
            
        except (KeyError, ValueError):
            pass
        
        return HttpResponseRedirect(reverse("strekmann_menu_list", args=[id]))
    else:
        menu = get_object_or_404(Menu, pk=id)
        
    tree_id = menu.tree_id
    menu = menu.get_descendants().all()
    menus = Menu.tree.root_nodes().all()
    return render_to_response('strekmann_menu/list.html', 
        {
            'menu': menu,
            'menus': menus,
            'id': id,
            'tree_id': tree_id,
        }, 
        context_instance=RequestContext(request))
      

  
def new_menuitem(request, tree_id):
    """Create a new menu item - return html for ajax injection"""
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.user = request.user
            menu.insert_at(menu.parent, 'last-child', True)
        return HttpResponseRedirect(reverse("strekmann_menu_list", args=[Menu.tree.root_node(tree_id).pk]))
    else:
        menu = Menu()
        menu.tree_id = tree_id
        form = MenuForm(instance=menu)
    
    return render_to_response(
        'strekmann_menu/new_item.html', 
        {'form': form, 'tree_id': tree_id}, 
        context_instance=RequestContext(request))