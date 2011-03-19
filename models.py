from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel

class Menu(MPTTModel):
    """MPTT tree menu"""
    name = models.CharField(max_length=20)
    url = models.URLField(blank=True, verify_exists=True)
    user = models.ForeignKey(User)
    updated_date = models.DateTimeField(auto_now=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')

    class Meta:
        ordering = ["name"]
        verbose_name, verbose_name_plural = "menu", "menus"
        
    class MPTTMeta:
        pass
        #order_insertion_by=['name']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('Menu', [self.id])

