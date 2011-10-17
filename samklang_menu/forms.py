from django.forms import ModelForm
from samklang_menu.models import Menu

class MenuForm(ModelForm):
    
    class Meta:
        model = Menu
        fields = ('name', 'url', 'parent')
