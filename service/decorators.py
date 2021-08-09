from django.core.exceptions import PermissionDenied



def user_is_company(function):
    def check(request, *args, **kwargs):
        if request.user.profile.is_company:
            pass
        else:
            raise PermissionDenied

def user_is_manufacturer(function):
    def check(request, *args, **kwargs):
        if request.user.profile.is_manufacturer:
            pass
        else:
            raise PermissionDenied
