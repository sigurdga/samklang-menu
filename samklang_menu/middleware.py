
class LazyActive(object):
    def __get__(self, request, obj_type=None):
        if not hasattr(request, '_cached_active'):
            from samklang_menu.models import Menu

            request._cached_active = Menu.find_active(request.site, request.path_info)
        return request._cached_active

class ActivePageMiddleware(object):
    def process_request(self, request):
        request.__class__.active = LazyActive()
        return None

