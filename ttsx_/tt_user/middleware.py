#!----/usr/bin/env ipython3---

class UrlMiddleWare:
    def process_view(self,request,view_func, view_args, view_kwargs):
        if request.path not in [
            '/user/register/',
            '/user/register_handle/',
            '/user/has_user',
            '/user/login/',
            '/user/logout/',
            '/user/login_handle/',
        ]:
            request.session['lastpath'] = request.get_full_path()