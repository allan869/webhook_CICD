**webhook开发说明**

叙述：

    gitlab提交代码自动触发此功能（许在gitlab中配置webhook地址和功能），然后触发Jenkins自动构建，判断Jenkins是否构建成功（docker镜像pull到reg仓库），成功后marathon修改其对应项目的值自动部署此项目

功能需求：

    1.Jenkins接口

    2.处理接收gitlab数据

    3.项目命名规则

    4.日志

    5.异常处理

    6.构建方式分析处理

    7.固定分支处理

    8.开关

部署：

    1.docker容器运行
    