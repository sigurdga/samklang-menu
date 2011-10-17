from django.db import models
from django.contrib.auth.models import User, Group
from mptt.models import MPTTModel

class Menu(MPTTModel):
    """MPTT tree menu"""
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=100, db_index=True)
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group, null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    class Meta:
        ordering = ["name"]
        verbose_name, verbose_name_plural = "menu", "menus"
        db_table = 'samklang_menu'

    class MPTTMeta:
        pass

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('Menu', [self.id])

