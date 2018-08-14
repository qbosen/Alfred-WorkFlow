## MavenRepo 在 mvnRepository 中查找依赖

本来已经写了一个 [FindMaven][findMavenReadeMe] 插件了, 但是不得不说 阿里云和 CentralMaven 的相关性搜索太差了。

因为 `mvnRepository` 没有找到查询接口, 同时也需要二次查询, 所以单独写了一个插件

因为网络文件，所以速度比较慢。可以设置 `Alfred proxy` 解决。 **已经添加了缓存机制**

```
MvnRepo 可以搜索 Java Library 并复制配置，或者在浏览器打开。
支持的 Repo: mvnrepository.com

支持的操作:
1. return: 			复制 gradle 配置 group:name:version
2. alt + return: 	复制 Maven 配置
3. ctrl + return: 	复制 gradle 配置
4. cmd + return: 	打开浏览器，在 mvnrepository 中查看详情
5. 在 versions 中匹配结果
6. 对 versions 结果进行缓存

支持的配置:

1. 快捷键:	默认快捷键为 mvn 可以在 WorkFlow 的环境变量修改配置:
 			{keyword:mvn}

2. 搜索版本:	默认显示所有版本号, 设置 {step_version:true} 后，
			只显示每个大版本的最新版本

3. 显示占位:	{holder:version} 可以设置在版本搜索中，显示的关键字

4. 缓存周期:	{cache_days:30} 可以设置缓存的天数，小于等于`0`关闭缓存，
			对相同内容的搜索，如果超过设置天数就重新从网页获取
```

❍ 1. 对 scope 进行适配 @added(18-08-12 11:20)

✔ 2. 支持对 version 进行过滤  @done(18-08-14 12:29)

✔ 3. 支持 cache 缓存  @done(18-08-14 15:02)

❍ 4. 手动清除缓存(存在缓存时修改`step_version`设置,需要手动清理) @added(18-08-14 15:19)


[findMavenReadeMe]:[https://github.com/qbosen/Alfred-WorkFlow/blob/master/FindMaven/README.md]