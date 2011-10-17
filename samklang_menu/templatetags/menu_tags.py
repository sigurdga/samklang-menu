from samklang_menu.models import Menu
from django import template

register = template.Library()

def make_menu(parent, user):
    menu = []
    for child in parent.get_children():
        if not child.group or child.group in user.groups.all():
            menu.append(child)
    return menu

def html_menu(menu):
    return "<ul>" + "".join([ '<li><a href="%s">%s</a></li>' % (item.url, item.name) for item in menu ]) + "</ul>"

@register.simple_tag
def menu(request, default_url="/"):
    if hasattr(request, 'site'):
        site_id = request.site.id
    else:
        site_id = 1
    user = request.user
    path = request.path_info
    try:
        active_link = Menu.objects.get(tree_id=site_id, url=path)
        menu = make_menu(active_link, user)
        while not menu and active_link.parent: #empty?
            active_link = active_link.parent
            menu = make_menu(active_link, user)
    except Menu.DoesNotExist:
        active_link = Menu.objects.get(tree_id=site_id, url=default_url)
        menu = make_menu(active_link, user)
        while not menu and active_link.parent:
            active_link = active_link.parent
            menu = make_menu(active_link, user)

    return html_menu(menu)

@register.simple_tag
def breadcrumbs(request, extra=[]):
    """Get the menu item for the page you are at. Find all ancestors in the menu hierarchy. Start at top level and break if permissions are not ok.

    You can pass extra elements using the "extra" parameter"""

    if hasattr(request, 'site'):
        site_id = request.site.id
    else:
        site_id = 1
    user = request.user
    path = request.path_info
    try:
        link = Menu.objects.get(tree_id=site_id, url=path)
    except Menu.DoesNotExist:
        link = Menu.objects.get(tree_id=site_id, url='/')

    ancestors = []
    for ancestor in link.get_ancestors():
        if not ancestor.group or ancestor.group in user.groups.all():
            ancestors.append(ancestor)
        else:
            break
    ancestors.append(link)

    return " > ".join([ '<a href="%s">%s</a>' % (ancestor.url, ancestor.name) for ancestor in ancestors ] + [ '<a href="%s">%s</a>' % (t[0], t[1]) for t in extra ])

