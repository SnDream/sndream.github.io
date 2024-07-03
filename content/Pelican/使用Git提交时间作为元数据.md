Title: 使用Git提交时间作为元数据
Slug: git-commmit-as-metadata

目前已经正常了。

真是有够折腾的，GitHub的Action下载的仓库有权限问题，默认无法处理，尝试直接修改插件也不行，插件的某些调用绕过了环境变量设置，导致编译时工作不正常，需要在编译脚本中增加

```
export GIT_CONFIG_COUNT='1'
export GIT_CONFIG_KEY_0='safe.directory'
export GIT_CONFIG_VALUE_0='*'
```

才可以让插件工作正常。
后面考虑一下在插件中强制设置相关环境变量。
