## MavenRepo 在 mvnRepository 中查找依赖

本来已经有一个 [FindMaven][findMavenReadeMe] 了, 但是不得不说 阿里云和 CentralMaven 的相关性搜索太差了。

因为 mvnRepository 没有找到查询接口, 同时也需要二次查询, 所以单独写了一个 `Workflow` 插件

#### 18-8-12
[ ] 1. 对 scope 进行适配


[findMavenReadeMe]:[https://github.com/qbosen/Alfred-WorkFlow/blob/master/FindMaven/README.md]