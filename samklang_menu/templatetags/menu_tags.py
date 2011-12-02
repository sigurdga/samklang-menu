from samklang_menu.models import Menu
from django import template
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

def make_menu(parent, user):
    menu = []
    for child in parent.get_children():
        if not child.group or child.group in user.groups.all():
            menu.append(child)
    return menu

def html_menu(menu, active_link=None):
    menu_contents = []
    for item in menu:
        if item==active_link:
            class_expr = 'class="active"'
        else:
            class_expr = ''
        menu_contents.append('<li><a href="%s" %s>%s</a></li>' % (item.url, class_expr, item.name))
    return "<ul>" + "".join(menu_contents) + "</ul>"

def find_active(site_id, path):
    """
    Find active link by stripping off one part of the url at a time.
    """
    active_link = None
    while not active_link and active_link != "/":
        try:
            active_link = Menu.objects.get(tree_id=site_id, url=path)
            break
        except ObjectDoesNotExist:
            if path.endswith("/"):
                path = path.rsplit("/", 2)[0] + "/"
            else:
                path = path.rsplit("/", 1)[0] + "/"
    return active_link

def submenu(active_link, user):
    """
    Will actually get submenu of the first parent it can show
    """
    menu = make_menu(active_link, user)
    while not menu and active_link.parent:
        active_link = active_link.parent
        menu = make_menu(active_link, user)
    return menu

@register.simple_tag
def simple_menu(request, default_url="/"):

    if hasattr(request, 'site'):
        site_id = request.site.id
    else:
        site_id = 1

    # find the closest parent to the active url
    active_link = find_active(site_id, request.path_info)

    # find the menu closest to the active_link
    menu = submenu(active_link, request.user)

    if request.path_info != "/" and active_link.url == "/":
        active_link = None

    return html_menu(menu, active_link)

@register.simple_tag
def menu(request, default_url="/"):
    return simple_menu(request, default_url)


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

