from functools import wraps


def load_parent_resource_factory(modelcls, id_field: int):
    def decorated_view(func):
        @wraps(func)
        def wrapper(*wargs, **wkwargs):
            from ..webapp import db
            id = wkwargs.pop(id_field)
            if id:
                resource = db.get_or_404(modelcls, id)
                return func(resource, *wargs, **wkwargs)
            else:
                return func(*wargs, **wkwargs)
        return wrapper
    return decorated_view
