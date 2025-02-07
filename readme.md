##  蓝鲸Python Operator开发框架 (Bof)

---
[![license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](https://github.com/TencentBlueKing/bk-operator-framework/blob/master/LICENSE.txt)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/kopf.svg)](https://pypi.org/project/kopf/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/TencentBlueKing/bk-operator-framework/pulls)

[English Documents Available](readme_en.md)

Bof是一个使用 [自定义资源定义(CRD)](https://kubernetes.io/docs/tasks/access-kubernetes-api/extend-api-custom-resource-definitions) 来构建Kubernetes API的框架。

类似于Django和Flask等Web开发框架，Bof提高了开发速度，并减少了开发人员在使用Python语言快速构建和发布 Kubernetes API 时所需管理的复杂性。它基于构建核心Kubernetes API的规范技术，提供了简单的抽象，减少了样板代码和繁琐工作。

Bof并不是一个供复制粘贴的示例，而是提供了强大的库和工具，从头开始简化构建和发布 Kubernetes API 的过程。它提供了一个插件架构，使用户能够利用可选的辅助工具和功能。

Bof基于 [kopf](https://github.com/nolar/kopf.git) 和 [pydantic](https://github.com/pydantic/pydantic.git) 库开发。

## Roadmap
- [版本日志](docs/release.md)

## Support
- [蓝鲸论坛](https://bk.tencent.com/s-mart/community)
- [蓝鲸 DevOps 在线视频教程](https://bk.tencent.com/s-mart/video/)
- [蓝鲸社区版交流群](https://jq.qq.com/?_wv=1027&k=5zk8F7G)
  
## BlueKing Community
- [BK-CMDB](https://github.com/Tencent/bk-cmdb): 蓝鲸配置平台（蓝鲸 CMDB）是一个面向资产及应用的企业级配置管理平台。
- [BK-CI](https://github.com/Tencent/bk-ci): 蓝鲸持续集成平台是一个开源的持续集成和持续交付系统，可以轻松将你的研发流程呈现到你面前。
- [BK-BCS](https://github.com/Tencent/bk-bcs): 蓝鲸容器管理平台是以容器技术为基础，为微服务业务提供编排管理的基础服务平台。
- [BK-PaaS](https://github.com/Tencent/bk-PaaS): 蓝鲸 PaaS 平台是一个开放式的开发平台，让开发者可以方便快捷地创建、开发、部署和管理 SaaS 应用。
- [BK-SOPS](https://github.com/Tencent/bk-sops): 标准运维（SOPS）是通过可视化的图形界面进行任务流程编排和执行的系统，是蓝鲸体系中一款轻量级的调度编排类 SaaS 产品。
- [BK-JOB](https://github.com/Tencent/bk-job): 蓝鲸作业平台(Job)是一套运维脚本管理系统，具备海量任务并发处理能力。

## Contributing
如果您有好的意见或建议，欢迎给我们提 Issues 或 Pull Requests，为蓝鲸开源社区贡献力量。   
[腾讯开源激励计划](https://opensource.tencent.com/contribution) 鼓励开发者的参与和贡献，期待你的加入。

## License
基于 MIT 协议， 详细请参考 [LICENSE](LICENSE.txt)。
