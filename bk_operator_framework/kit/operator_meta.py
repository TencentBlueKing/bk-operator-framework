import inspect

from bk_operator_framework.constants import HandlerType, K8sResourceScope
from bk_operator_framework.hub.operator import OperatorHub


class OperatorMeta(type):
    def __new__(cls, name, bases, dct):
        # ensure initialization is only performed for subclasses of Plugin
        parents = [b for b in bases if isinstance(b, OperatorMeta)]
        if not parents:
            return super().__new__(cls, name, bases, dct)

        new_cls = super().__new__(cls, name, bases, dct)

        # meta validation
        meta_obj = getattr(new_cls, "Meta", None)
        if not meta_obj:
            raise RuntimeError("operator definition error, can not retrieve Meta attribute in {}".format(new_cls))

        # meta.singular validation
        singular = getattr(meta_obj, "singular", None)
        if not singular:
            raise RuntimeError(
                "operator definition error, can not retrieve [singular] field in {}.Meta".format(new_cls)
            )

        # meta.version validation
        version = getattr(meta_obj, "version", None)
        if not version:
            raise RuntimeError("operator definition error, can not retrieve [version] field in {}.Meta".format(new_cls))

        # meta.scope validation
        scope = getattr(meta_obj, "scope", None)
        if scope not in {K8sResourceScope.Namespaced, K8sResourceScope.Cluster}:
            raise RuntimeError("operator definition error, can not retrieve [scope] field in {}.Meta".format(new_cls))

        # meta.storage validation
        storage = getattr(meta_obj, "storage", None)
        if storage and not isinstance(storage, bool):
            raise RuntimeError(
                "operator definition error, [storage] field must be of bool type in {}.Meta".format(new_cls)
            )

        if not storage:
            setattr(meta_obj, "storage", True)

        # meta.served validation
        served = getattr(meta_obj, "served", None)
        if served and not isinstance(served, bool):
            raise RuntimeError(
                "operator definition error, [served] field must be of bool type in {}.Meta".format(new_cls)
            )
        if not served:
            setattr(meta_obj, "served", True)

        # meta.plural validation
        plural = getattr(meta_obj, "plural", None)
        if not plural:
            setattr(meta_obj, "plural", "{}s".format(singular))

        # meta.description validation
        description = getattr(meta_obj, "description", None)
        if not description:
            setattr(meta_obj, "description", "operator description")

        # meta.kind validation
        kind = getattr(meta_obj, "kind", None)
        if not kind:
            setattr(meta_obj, "kind", singular.capitalize())

        # meta.listKind validation
        listKind = getattr(meta_obj, "listKind", None)
        if not listKind:
            setattr(meta_obj, "listKind", "{}List".format(meta_obj.kind))

        # meta.group validation
        group = getattr(meta_obj, "group", None)
        if not group:
            setattr(meta_obj, "group", "dev.com")

        # meta.name validation
        name = getattr(meta_obj, "name", None)
        if not name:
            setattr(meta_obj, "name", "{}.{}".format(meta_obj.plural, meta_obj.group))

        # meta.shortNames validation
        shortNames = getattr(meta_obj, "shortNames", None)
        if shortNames and not isinstance(shortNames, list):
            raise RuntimeError(
                "operator definition error, [shortNames] field must be of list type in {}.Meta".format(new_cls)
            )

        # meta.annotation_prefix validation
        annotation_prefix = getattr(meta_obj, "annotation_prefix", None)
        if not annotation_prefix:
            setattr(meta_obj, "annotation_prefix", "{}.bof.dev.com".format(meta_obj.plural))

        # set custom  handler list
        handler_list = []
        exist_webhook_handler = False
        for method_name, method in inspect.getmembers(new_cls, predicate=inspect.isfunction):
            setattr(method, "version", version)

            if method_name == "webhook_configure":
                continue
            handler_type = getattr(method, "handler_type", None)
            if handler_type:
                if handler_type in {HandlerType.Mutate, HandlerType.Validate}:
                    method.handler_kwargs.setdefault("id", method.__name__.replace("_", "-"))
                    exist_webhook_handler = True
                handler_list.append(method)

        if exist_webhook_handler:
            handler_list.append(new_cls.webhook_configure)

        new_cls._set_handler_list(handler_list)
        OperatorHub._register_operator(new_cls)

        return new_cls
