from django.forms import ModelForm
from strekmann_menu.models import Menu

class MenuForm(ModelForm):
    
    class Meta:
        model = Menu
        fields = ('name', 'url', 'parent')