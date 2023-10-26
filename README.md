# 🧐bk-operator-framework

bk-operator-framework 是一个轻量化的Kubernetes Operator开发的框架和库。 开发者只需要几行python代码就可以完成一个Kubernetes Operator的开发！！！

# 🚀快速开始

## 创建你的第一个项目

```shell
pip install bk_operator_framework

bof init {Your Operator Project Name}
```

# 🧾基础概念

## Operator构成

一个Operator由以下元素构成

- Meta：Operator元数据，用来定义CRD的version、singular、kind、scope等属性以及其他一些全局配置
- Spec：Operator CR的Spec(输入)模型
- Status: Operator CR的Status(输出)模型
- RBAC：Operator 操作其他K8s资源所需要的权限

## Operator项目结构

```
├── bk_operator
│   ├── __init__.py
│   └── versions
│       ├── __init__.py
│       └── v1.py
├── .dockerignore
├── .gitignore
├── Dockerfile
└── requirements.txt
```

### 你需要关注的

- bk_operator/versions：存放每个版本的Operator定义，所有Operator定义必须位于该目录下，目录下文件名不做限制，框架会自动从该目录下发现Operator
- requirements.txt：Operator需要依赖的第三方库

### 你不需要（不应该）关注的

- Dockerfile：构建Operator Docker 镜像时的描述文件
- .gitignore：排除不需要Git版本控制的文件
- .dockerignore：构建 Operator Docker 镜像时应忽略的文件和目录

# 1. 📚如何开发Operator

## 定义Operator

所有的Operator都需要继承 `bk_operator_framework.kit.Operator`，如下所示

```python
from bk_operator_framework.kit import Operator


class ExampleOperator(Operator):
    pass
```

## Operator元数据

在每个Operator类中我们需要定义 `Meta` 内部类，其中包含该版本Operator的元数据：

- singular: Operator CRD `spec.names.singular`
- kind: Operator CRD `spec.names.kind`
- scope: Operator CRD `spec.scope`
- version：Operator CRD `spec.versions[0].name`
- group(可选):  Operator CRD `spec.group`，默认为`dev.com`
- plural(可选): Operator CRD `spec.names.plural`
- name(可选): Operator CRD `spec.metadata.name`，默认为`{plural}.{group}`
- listKind(可选): Operator CRD `spec.names.listKind`，默认为`{kind}List`
- storage(可选): Operator CRD `spec.versions[0].storage`，默认为`True`
- served(可选): Operator CRD `spec.versions[0].served`，默认为`True`
- shortNames(可选): Operator CRD `spec.names.shortNames`,默认为`[]`

```python
from bk_operator_framework.kit import Operator, K8sResourceScope


class ExampleOperator(Operator):
    class Meta:
        version = "v1"
        singular = "example"
        kind = "Example"
        scope = K8sResourceScope.Cluster
```

## 声明CR的Spec模型

每个Operator都需要包含一个继承自 `bk_plugin_framework.kit.SpecModel` 的内部类 `Spec` 来声明该CRD对应CR的Spec模型，Spec的作用如下：

- 声明Operator CRD对应CR的Spec字段，字段类型类型以及字段说明

```python
from bk_operator_framework.kit import Operator, SpecModel, Field


class ExampleOperator(Operator):
    ...

    class Spec(SpecModel):
        message: str = Field(description="A example string field", default="Hello World")

    ...
```

### CR的Spec模型定义说明(可选)

```python
import typing
from bk_operator_framework.kit import SpecModel, Field, BaseModel


class Spec(SpecModel):
    class EgObjectModel(BaseModel):
        hello: str = Field(description="A EgObjectModel string field")

    message: str = Field(description="A example string field", default="Hello World")
    eg_int: int = Field(description="A example int field")
    eg_list: typing.List[str] = Field(description="A example list field")
    eg_bool: bool = Field(description="A example bool field", default=False)
    eg_object: EgObjectModel = Field(description="A example object field")
```

## 声明CR的Status模型

每个插件都需要包含一个继承自 `bk_plugin_framework.kit.StatusModel` 的内部类 `Status` 来声明该插件的输入模型，输入模型的作用如下：

- 声明Operator CRD对应CR的status字段

**CR的Status模型的定义方式与Spec定义方式相同，只是基类不同**

```python
from bk_operator_framework.kit import Operator, StatusModel, Field


class ExampleOperator(Operator):
    ...

    class Spec(StatusModel):
        message: str = Field(description="A example string field", default="Hello World")

    ...
```

## 声明Operator Handler

使用框架的 `bk_operator_framework.kit.handler` 的装饰器来声明要k8s的资源变化时要执行的handler函数 handler装饰器参数说明：

- handler_type: 要处理函数触发的事件类型
- singular(可选): 要处理函数触发的CR的单数名称
- plural(可选): 要处理函数触发的CR的复数名称
- version(可选): 要处理函数触发的CR的版本
- group(可选): 要处理函数触发的CR的API组
- field(可选): 要处理函数触发的资源字段。如果指定，只有当该字段发生更改时，才会调用处理函数。eg `field=spec.message`,处理函数只会在CR的spec.message进行调用
- when(可选): 用于确定是否应该调用处理函数。函数应该接受一个CR，并返回一个布尔值。如果函数返回 True，处理函数触发；否则，忽略事件。
- namespace(可选)：要handler逻辑触发的CR的命名空间。默认为所有的命令空间
- retries(可选): 一个整数，指定处理函数的重试次数。如果处理函数失败，将根据此值进行重试。默认为1，不进行重试

**在这里，我将为您提供一些使用Operator Handler的示例。我们将继续使用`ExampleOperator`作为基础，并为每个HandlerType添加处理函数。**

1. `HandlerType.Event`:
    - 当监听资源的cr发生`DELETED/ADDED/MODIFIED`时执行handler
    - 当Operator Server启动的时候,监听资源的所有cr触发一次handler，此时事件类型为`None`
    - *注意: 确保 HandlerType.Event 装饰的 handler 方法是幂等的，即多次调用具有相同的效果。这是因为 Kubernetes 控制器可能会多次调用 handler
      方法，甚至在资源没有发生变化的情况下也可能调用*
    - 示例:
   ```python
    from bk_operator_framework.kit import Operator, handler, HandlerType
    
    import logging
    
    logger = logging.getLogger("bk-operator")
    
    class ExampleOperator(Operator):
        ...
        @handler(HandlerType.Event, version="v1", group="dev.com", plural="examples")
        def reconcile(self, spec, name, **kwargs):
            event_type = kwargs.get("event", {}).get("type")
            logger.info(f"service-bind-polaris cr [{event_type}] reconcile event spec: {spec}")
        ...
    ```
2. `HandlerType.Create`
    - 当监听资源的cr创建时执行handler
    - 示例:
   ```python
    from bk_operator_framework.kit import Operator, handler, HandlerType
    
    import logging
    
    logger = logging.getLogger("bk-operator")
    
    class ExampleOperator(Operator):
        ...
        @handler(HandlerType.Create, version="v1", group="dev.com", plural="examples")
        def create(self, spec, **kwargs):
            logger.info(f"create spec: {spec}")
        ...
    ```
3. `HandlerType.Update`
    - 当监听资源的cr更新时执行handler
    - 可以通过`field="spec"`指定当CR资源examples的特定字段（例如，spec）更新时执行handler
    - 示例:
   ```python
    from bk_operator_framework.kit import Operator, handler, HandlerType
    
    import logging
    
    logger = logging.getLogger("bk-operator")
    
    class ExampleOperator(Operator):
        ...
        @handler(HandlerType.Update, version="v1", group="dev.com", plural="examples", field="spec")
        def update(self, spec, **kwargs):
            logger.info(f"update spec: {spec}")
        ...
    ```
4. `HandlerType.Delete`
    - 当监听资源的cr删除时执行handler
    - **注意：`HandlerType.Delete` 的 handler 会自动注入 finalizer 以确保在删除资源之前执行清理操作。如果添加了`HandlerType.Delete` 的
      handler，但不需要finalizer来阻止实际删除，则可以将可选参数 `option=True` 传递给handler装饰器。**
    - 示例:
   ```python
    from bk_operator_framework.kit import Operator, handler, HandlerType
    
    import logging
    
    logger = logging.getLogger("bk-operator")
    
    class ExampleOperator(Operator):
        ...
        @handler(HandlerType.Delete, version="v1", group="dev.com", plural="examples")
        def delete(self, spec, **kwargs):
            logger.info(f"delete spec: {spec}")
        ...
    ```

5. `HandlerType.Mutate`
    - 自动注册一个`Admission Webhook` 当监听资源的CR创建或更新前执行handler函数，用于修改请求中的对象
    - **注意：如果`HandlerType.Mutate`的handler抛出了没有捕获的异常，监听的CR对象将会创建/更新失败**
    - 示例:
   ```python
    from bk_operator_framework.kit import Operator, handler, HandlerType
    
    import logging
    
    logger = logging.getLogger("bk-operator")
    
    class ExampleOperator(Operator):
        ...
        @handler(HandlerType.Mutate, version="v1", group="dev.com", plural="examples")
        def mutate(self, spec, **kwargs):
            logger.info(f"mutate spec: {spec}")
        ...
    ```

6. `HandlerType.Validate`
    - 自动注册一个`Admission Webhook` 当监听资源的CR创建或更新前执行handler函数，用于验证请求中的对象是否符合预期条件和规则
    - **注意：如果`HandlerType.Validate`的handler抛出了没有捕获的异常，监听的CR对象将会创建/更新失败**
    - 示例:
   ```python
    from bk_operator_framework.kit import Operator, handler, HandlerType
    
    import logging
    
    logger = logging.getLogger("bk-operator")
    
    class ExampleOperator(Operator):
        ...
        @handler(HandlerType.Validate, version="v1", group="dev.com", plural="examples")
        def validate(self, spec, **kwargs):
            logger.info(f"validate spec: {spec}")
        ...
    ```

## 当Operator Handler依赖于其他CR资源变化时
当Operator自身的Handler逻辑需要其他CR资源变化执行时，您可以使用`self.request_handler`来执行自己定义的handler逻辑  
示例:  
当pod发生变化时我们调用一次我们自身的`reconcile`函数
```python
from bk_operator_framework.kit import Operator, handler, HandlerType

import logging

logger = logging.getLogger("bk-operator")


class ExampleOperator(Operator):
    ...

    @handler(HandlerType.Event, version="v1", group="dev.com", plural="examples")
    def reconcile(self, spec, name, **kwargs):
        event_type = kwargs.get("event", {}).get("type")
        logger.info(f"example cr [{event_type}] reconcile event spec: {spec}")

    @handler(HandlerType.Event, plural="pods")
    def watch_pods(self, **kwargs):
        event_type = kwargs.get("event", {}).get("type")
        if event_type in {"DELETED", "ADDED", "MODIFIED"}:
            self.request_handler("cr_name")

    ...
 ```

## 构建helm包，镜像构建，预览Operator CRD/RBAC/APP等Yaml定义

```shell
usage: bof build [-h] [-t TARGET_STRING] [--skip-image] [--push-image]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET_STRING, --target_string TARGET_STRING
                        Set the target build stage to build, eg. <docker_hub_username>/<repository_name>:<tag>
  --skip-image          Skip docker build to build image>
  --push-image          push image to docker hub
```

## helm包部署

```shell
helm install examples helm_charts/{verison}
```