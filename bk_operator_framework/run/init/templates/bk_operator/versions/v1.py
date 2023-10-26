import logging

from bk_operator_framework.kit import (
    Field,
    HandlerType,
    K8sResourceScope,
    Operator,
    SpecModel,
    StatusModel,
    handler,
)

logger = logging.getLogger("bk-operator")


class ExampleOperator(Operator):
    CUSTOM_ENVIRONMENT_KEY = ["TEST"]

    class Meta:
        version = "v1"
        singular = "example"
        kind = "Example"
        scope = K8sResourceScope.Cluster

    class Spec(SpecModel):
        message: str = Field(description="A example string field", default="Hello World")

    class Status(StatusModel):
        showMessage: bool = Field(description="Whether the message is showed")

    @handler(HandlerType.Event, plural="examples")
    def reconcile(self, memo, spec, **kwargs):
        logger.info(f"event spec: {spec}, {kwargs.get('name')}")
