from flask import session, redirect
from functools import wraps


def require_authentication(api_method):
    @wraps(api_method)
    def check_authentication(*args, **kwargs):
        if 'auth_user' not in session or session['auth_user'] == {}:
            return redirect('/login', 302)
        else:
            return api_method(*args, **kwargs)

    return check_authentication


def require_admin_authentication(api_method):
    @wraps(api_method)
    def check_admin_authentication(*args, **kwargs):
        if 'auth_user' not in session or session['auth_user'] == {} or 'isAdmin' not in session['auth_user']:
            return redirect('/login', 302)
        else:
            return api_method(*args, **kwargs)
    return check_admin_authentication
