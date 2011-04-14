from django.forms import ModelForm
from s7n.menu.models import Menu

class MenuForm(ModelForm):
    
    class Meta:
        model = Menu
        fields = ('name', 'url', 'parent')