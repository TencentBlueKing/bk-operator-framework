import copy
import time

import kopf
from pydantic import BaseModel

from bk_operator_framework.constants import HandlerType, K8sResourceScope
from bk_operator_framework.kit import k8s_utils
from bk_operator_framework.kit.decorators import handler
from bk_operator_framework.kit.operator_meta import OperatorMeta
from bk_operator_framework.utils.cert import generate_certificate


class SpecModel(BaseModel):
    pass


class StatusModel(BaseModel):
    pass


class RBACModel(object):
    # eg. [{"apiGroups": ["kopf.dev"], "resources": ["kopfexamples"], "verbs": ["list", "watch"]}]
    extra_role_rules = []
    service_account = {}


class Operator(metaclass=OperatorMeta):
    CUSTOM_ENVIRONMENT_KEY = []

    _EMPTY_SCHEMA = {"type": "object", "properties": {}, "required": [], "definitions": {}}
    _JSON_SCHEMA_KEY_LIST = [
        "type",
        "default",
        "description",
        "items",
        "properties",
        "print_column",
        "print_column__name",
        "print_column__priority",
    ]

    __handler_list = []

    def __init__(self, *args, **kwargs):
        self.status = dict(kwargs["status"]) if "status" in kwargs else {}
        self.cr_name = kwargs.get("meta", {}).get("name")
        self.namespace = kwargs.get("meta", {}).get("namespace")

    class Error(Exception):
        pass

    def request_handler(self, cr_name, cr_namespace=None):
        """
        在CR依赖的其他资源发生变化时请求一个CR处理函数
        :param cr_name:
        :param cr_namespace
        :return:
        """
        if cr_namespace is None:
            cr_namespace = k8s_utils.get_current_namespace()

        cr_kwargs = {
            "group": self.Meta.group,
            "version": self.Meta.version,
            "plural": self.Meta.plural,
            "name": cr_name,
            "annotations": {f"{self.Meta.annotation_prefix}/request_handler": f"{time.time() * 1000000}"},
        }
        if self.Meta.scope == K8sResourceScope.Cluster:
            k8s_utils.patch_cluster_cr_annotations(**cr_kwargs)

        if self.Meta.scope == K8sResourceScope.Namespaced:
            cr_kwargs.update({"namespace": cr_namespace})
            k8s_utils.patch_namespaced_cr_annotations(**cr_kwargs)

    def update_status(self, cr_namespace=None):
        """
        更新 Operator 定义的 CR Status
        :return:
        """
        if cr_namespace is None:
            cr_namespace = self.namespace

        cr_kwargs = {
            "group": self.Meta.group,
            "version": self.Meta.version,
            "plural": self.Meta.plural,
            "name": self.cr_name,
            "status": self.status,
        }
        if self.Meta.scope == K8sResourceScope.Cluster:
            k8s_utils.patch_cluster_cr_status(**cr_kwargs)

        if self.Meta.scope == K8sResourceScope.Namespaced:
            cr_kwargs.update({"namespace": cr_namespace})
            k8s_utils.patch_namespaced_cr_status(**cr_kwargs)

    @handler(HandlerType.Startup)
    def start_up(self, settings: kopf.OperatorSettings, **_):
        settings.persistence.finalizer = "{}/KopfFinalizerMarker".format(self.Meta.annotation_prefix)
        settings.persistence.progress_storage = kopf.SmartProgressStorage(prefix=self.Meta.annotation_prefix)
        settings.persistence.diffbase_storage = kopf.AnnotationsDiffBaseStorage(prefix=self.Meta.annotation_prefix)

    @handler(HandlerType.Startup)
    def webhook_configure(self, settings: kopf.OperatorSettings, **kwargs):
        current_pod_ip = k8s_utils.get_current_pod_ip()
        private_key_file_path, cert_file_path = generate_certificate([current_pod_ip])
        webhook_info = {
            "port": 9443,
            "addr": current_pod_ip,
            "certfile": cert_file_path,
            "pkeyfile": private_key_file_path,
        }
        settings.admission.server = kopf.WebhookServer(**webhook_info)
        settings.admission.managed = "{}.{}.admission.hook".format(self.Meta.singular, self.Meta.version)

    @classmethod
    def _trim_schema(cls, schema) -> dict:
        def _trim_properties(_properties):
            if "allOf" in _properties:
                _child_cls_name = _properties["allOf"][0]["$ref"].split("/")[-1]
                _properties.update(schema["$defs"][_child_cls_name])
                for _k, _v in _properties["properties"].items():
                    _properties["properties"][_k] = _trim_properties(_v)

            if "items" in _properties and "$ref" in _properties["items"]:
                _child_cls_name = _properties["items"]["$ref"].split("/")[-1]
                _properties["items"].update(schema["$defs"][_child_cls_name])
                for _k, _v in _properties["items"]["properties"].items():
                    _properties["items"]["properties"][_k] = _trim_properties(_v)

            __properties = copy.deepcopy(_properties)
            for _k, _v in _properties.items():
                if _k not in cls._JSON_SCHEMA_KEY_LIST:
                    __properties.pop(_k)

            for _k, _v in _properties.get("items", {}).items():
                if _k not in cls._JSON_SCHEMA_KEY_LIST:
                    __properties["items"].pop(_k)

            return __properties

        properties = {}
        for k, v in schema["properties"].items():
            properties[k] = _trim_properties(v)

        return {
            "type": schema["type"],
            "properties": properties,
            "required": schema.get("required", []),
            "definitions": schema.get("definitions", {}),
        }

    @classmethod
    def _set_handler_list(cls, handler_list):
        cls.__handler_list = handler_list

    @classmethod
    def get_handler_list(cls) -> list:
        return cls.__handler_list

    @classmethod
    def _get_spec_schema(cls) -> dict:
        spec_cls = getattr(cls, "Spec", None)
        if not spec_cls:
            return cls._EMPTY_SCHEMA

        spec_schema = cls._trim_schema(spec_cls.model_json_schema())
        return spec_schema

    @classmethod
    def _get_status_schema(cls) -> dict:
        status_cls = getattr(cls, "Status", StatusModel)
        status_schema = cls._trim_schema(status_cls.model_json_schema())
        return status_schema

    @classmethod
    def _get_rbac_schema(cls) -> dict:
        rbac_cls = getattr(cls, "RBAC", RBACModel)

        rbac_cls.service_account.setdefault("name", "{}-service-account".format(cls.Meta.singular))

        return {"service_account": rbac_cls.service_account, "extra_role_rules": rbac_cls.extra_role_rules}
