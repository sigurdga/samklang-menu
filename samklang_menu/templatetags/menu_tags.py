from samklang_menu.models import Menu
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site

register = template.Library()

def html_menu(menu, active_link=None):
    menu_contents = []
    for item in menu:
        if item==active_link:
            class_expr = 'class="active"'
        else:
            class_expr = ''
        menu_contents.append('<li><a href="%s" %s>%s</a></li>' % (item.url, class_expr, item.name))
    return "<ul>" + "".join(menu_contents) + "</ul>"


@register.simple_tag(takes_context=True)
def simple_menu(context):
    request = context['request']

    if hasattr(request, 'site'):
        site = request.site
    else:
        site = Site.objects.get(pk=1)

    # find the closest parent to the active url
    active_link = Menu.find_active(site, request.path_info)

    # find the menu closest to the active_link
    if active_link:
        menu = active_link.submenu(request.user)
    else:
        menu = Menu.objects.get(tree_id=site.id, url="/").submenu(request.user)

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

@register.simple_tag
def widgets(request, name):
    if request.active:
        return "".join([ widget.widget().render(request) for widget in request.active.widgets.filter(into_id=name) ])
    else:
        return ""
