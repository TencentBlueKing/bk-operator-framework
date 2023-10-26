import typing


class OperatorHub:
    __hub = {}

    @classmethod
    def _register_operator(cls, operator_cls: typing.Type):
        version = operator_cls.Meta.version
        existed_operator_cls = cls.__hub.get(version)
        if existed_operator_cls:
            raise RuntimeError(
                "operator register error, {}'s version {} conflict with {}".format(
                    existed_operator_cls, version, operator_cls
                )
            )

        cls.__hub[version] = operator_cls

    @classmethod
    def _clear(cls):
        cls.__hub = {}

    @classmethod
    def all_versions(cls) -> typing.Dict[str, typing.Type]:
        operators = {}
        for version, operator_cls in cls.__hub.items():
            operators[version] = operator_cls
        return operators

    @classmethod
    def versions(cls) -> typing.List[str]:
        return sorted(cls.__hub.keys(), reverse=True)
