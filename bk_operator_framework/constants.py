class K8sResourceScope:
    Cluster = "Cluster"
    Namespaced = "Namespaced"


class HandlerType:
    Create = "create"  # 当 CR 被创建时触发
    Update = "update"  # 当 CR 被更新时触发
    Delete = "delete"  # 当 CR 被删除时触发
    Event = "event"  # 当 CR 生成 K8s 事件时触发
    Field = "field"  # 当 CR 指定字段发生更改时触发

    Timer = "timer"  # 在指定的时间间隔后触发
    Startup = "startup"  # 当Operator Server 启动时触发
    Cleanup = "cleanup"  # 当 Operator Server 停止时触发
    Resume = "resume"  # 当Operator Server启动后，对所有现有 CR 触发

    Mutate = "mutate"  # 当 CR 创建或更新资源之前触发,用于修改请求中的对象（如标签、注释或规格）
    Validate = "validate"  # 当 CR 创建或更新之前触发，用于验证请求中的对象是否符合预期条件和规则


class OperatorRuntimeState:
    # 正在执行
    RUNNING = "Running"
    # 执行成功
    SUCCESS = "Succeeded"
    # 执行失败
    FAILED = "Failed"
    # 等待执行
    WAITING = "Waiting"
