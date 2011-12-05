class Widget(object):

    def __init__(self, options, *args, **kwargs):
        super(Widget, self).__init__(*args, **kwargs)
        self.options = options

    def get_display_name(self):
        raise NotImplementedError

    def render(self, request):
        raise NotImplementedError

    def render_option_form(self):
        raise NotImplementedError

    def get_option_dict(self):
        return self.options
