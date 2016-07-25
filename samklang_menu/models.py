from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson
from mptt.models import MPTTModel, TreeForeignKey

class Menu(MPTTModel):
    """MPTT tree menu"""
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=100, db_index=True, help_text=_("Internal url starting with / or external url starting with http"))
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class Meta:
        ordering = ["name"]
        verbose_name, verbose_name_plural = "menu", "menus"
        db_table = 'samklang_menu'

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('Menu', [self.id])

    @classmethod
    def find_active(cls, site, path):
        """
        Find active link by stripping off one part of the url at a time.
        Important to not match "anything" to the site root.
        """

        active_link = None
        while not active_link:
            # special case empty input, which probably means root
            if path == "":
                path = "/"

            try:
                active_link = cls.objects.get(tree_id=site.id, url=path)
            except cls.DoesNotExist:
                if path.endswith("/"):
                    path = path.rsplit("/", 2)[0] + "/"
                else:
                    path = path.rsplit("/", 1)[0] + "/"

            # break out before "anything" is matched to root page
            if path == "/":
                break
        return active_link

    def make_menu(self, user):
        """
        Run this on a parent to get out all children.
        """

        menu = []
        for child in self.get_children():
            if not child.group or child.group in user.groups.all():
                menu.append(child)
        return menu

    def submenu(self, user):
        """
        Will actually get submenu of the first parent it can show
        """

        active_link = self
        menu = active_link.make_menu(user)
        while not menu and active_link.parent:
            active_link = active_link.parent
            menu = active_link.make_menu(user)
        return menu


class Widget(models.Model):
    page = models.ForeignKey(Menu, verbose_name=_('Linked page'), related_name='widgets')
    widget_name = models.CharField(max_length=30)
    into_id = models.CharField(max_length=20)
    position = models.IntegerField(verbose_name=_('position'))
    options = models.TextField(blank=True, verbose_name=_('options'))

    class Meta:
        verbose_name = _('Page widget')
        verbose_name_plural = _('Page widgets')
        ordering = ('position', 'widget_name')
	db_table = 'samklang_widget'

    def __unicode__(self):
        return u"%s: %s" % (self.widget_name, self.page.name)

    def widget(self):
        app, widget_name = self.widget_name.rsplit(".", 1)
        imp = __import__(app + ".widgets", globals(), locals(), [widget_name])
        widget_class = getattr(imp, widget_name)
        try:
            options = simplejson.loads(self.options)
        except:
            options = {}
        widget = widget_class(options)
        return widget
