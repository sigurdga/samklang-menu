from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.db import connection, transaction
from django.conf import settings

from samklang_menu.models import Menu
from samklang_menu.forms import MenuForm

def list_menu(request):

    tree_id = request.site.id
    root_node = Menu.objects.root_node(tree_id)
    if not root_node or not request.user.is_superuser:
        raise Http404

    if request.method == 'POST':
        try:
            # get tree from json-data
            tree = simplejson.loads(request.POST["mptt_tree"])

            # format tree, remove root-item and make root-parents = id
            root = None
            for node in tree:
                if node['parent_id'] == 'root':
                    node['parent_id'] = root_node.id
                if node['item_id'] == 'root':
                    root = node

            if root:
                tree.remove(root)

            cursor = connection.cursor()
            qn = connection.ops.quote_name
            opts = root_node._meta

            if settings.DATABASES['default']['ENGINE'].endswith("sqlite3"):
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
            else:
                cursor.executemany("""
                    UPDATE %(table)s
                    SET %(parent)s = %%(parent_id)s,
                        %(left)s = %%(left)s,
                        %(right)s = %%(right)s,
                        %(level)s = %%(depth)s
                    WHERE %(pk)s = %%(item_id)s AND %(tree_id)s = %(given_tree_id)s""" % {
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

        return HttpResponseRedirect(reverse("menu-list"))

    menu = root_node.get_descendants().all()

    return render_to_response('samklang_menu/list.html',
        {
            'root': root_node,
            'menu': menu,
        },
        context_instance=RequestContext(request))



def new_menuitem(request):
    """Create a new menu item - return html for ajax injection"""
    tree_id = request.site.id
    if request.method == 'POST' and request.user.is_superuser:
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            if not Menu.objects.filter(tree_id=tree_id, url=menu.url):
                menu.user = request.user
                menu.insert_at(menu.parent, 'last-child', True)
            #TODO: invalidate
        return HttpResponseRedirect(reverse("menu-list"))
    else:
        menu = Menu()
        menu.tree_id = tree_id
        if request.method == 'GET' and 'parent_id' in request.GET:
            menu.parent_id = request.GET['parent_id']
        form = MenuForm(instance=menu)

    return render_to_response(
        'samklang_menu/new_item.html',
        {'form': form},
        context_instance=RequestContext(request))

def delete_menuitem(request):
    """Delete a menu item"""
    tree_id = request.site.id
    if request.method == 'POST' and 'node_id' in request.POST and request.user.is_superuser:
        node = Menu.objects.get(pk=request.POST['node_id'], tree_id=tree_id)
        node.delete()
        return HttpResponse("1")

    return HttpResponse("0")
