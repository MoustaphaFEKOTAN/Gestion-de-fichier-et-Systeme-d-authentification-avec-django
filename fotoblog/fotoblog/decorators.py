from django.http import HttpResponseForbidden
from functools import wraps
from django.shortcuts import redirect
# Vérifie que l'utilisateur a le rôle "creator"
def creator_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if getattr(request.user, "role", None) != "creator":
            # return redirect('no_access')
            return HttpResponseForbidden("Accès réservé aux créateurs.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# Vérifie que l'utilisateur est propriétaire de l'objet
def owner_required(model_class):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, pk, *args, **kwargs):
            obj = model_class.objects.get(pk=pk)
            if obj.owner != request.user:
                return HttpResponseForbidden("Vous n'êtes pas autorisé à modifier cet objet.")
            return view_func(request, pk, *args, **kwargs)
        return _wrapped_view
    return decorator
