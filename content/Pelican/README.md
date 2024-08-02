Title: 站点自述文件
Slug: readme
Summary: 站点的自述文件

> 本文主要用于站点这个仓库本身的自述文件。但也作为站点的文章提供。

# 站点概况

使用 `Pelican` 搭建的站点，用于记录 `GameBoy编程` 和 `Opendingux模拟器` 的一些条目。或许还有一些个人的牢骚。

由于用 `Pelican` 搭建站点的过程中也踩了不少坑，所以目前也记录一些搭建相关的内容。看了一下比正经内容还多。

（ ~~也许后面还会增加 J2ME 游戏的反编译拆解，另说呢，我连 JAVA 都还不会。~~ ）

# 仓库结构

下面简单说明仓库结构， ~~如果有人也想用 Pelican 照着搭建自己的站点的话，可能可以少踩点坑~~ 。

部分内容并非最佳实践，将会说明。

```
|__ .github
│   \__ workflows
│       \__ pelican.yml     -> Github Pages 自动构建
|__ pelicanconf.py          -> 编译配置
|__ requirements.txt        -> 构建依赖
|__ plugins                 -> 插件
│   |__ auto_attach             -> 自动转换
│   |__ filetime_from_git       -> 根据 Git 提交时间自动分配时间
│   |__ i18n_subsites           -> 多语言
│   |__ pelican_md_checklist    -> Markdown 复选框支持 (已废弃)
│   |__ plain_text_summary      -> 纯文本概要
│   \__ featured_image      -> 专题图片
|__ themes                  -> 主题
|   \__ Flex                    -> Flex 主题
|__ README.md               -> 自述文件
|__ content                 -> 站点内容
|   |__ assets                  -> 站点元素
|   |__ images                  -> 站点图像
|   \__ ...                     -> 站点文章
\__ ...                     -> (自动构建生成的文件等，忽略)
```

## 搭建目标

复选框用于标注已完成项。

- [x] 使用 Github Pages 自动构建。
- [x] 直接用构建结果部署，不要将编译结果提交到仓库中，更不要手动编译再将结果推送到仓库。
- [x] 单个仓库（包含submodules）就可以完成编译。
- [x] 只关联必须的插件。
    - 不太想将整个 `pelican-plugins` 仓库包含在内。
- [x] 选择合适的主题。
- [x] 直接编写 `Markdown` 文件。
    - 可以在 Github 网页上手动创建 `Markdown` 文件编写，不需要额外的依赖。
- [x] 编写的 `Markdown` 文件中链接的相对路径文档/图片在 Github 预览中和站点构建中都能同时工作。
- [x] 不需要手动写时间的元数据，直接依赖 Git 提交历史生成

## 自动构建

在 `.github/workflows/pelican.yml` 中。基本上遵照 Github 官方的 `Jekyll` 编译工作流，换成 `Pelican` 相关的环境和命令。

过程中使用[单独的构建工作流](https://github.com/SnDream/pelican-build-pages)完成编译。

编译环境使用 `Python 3.10.12` ，与我目前的环境上使用的一致。

编译过程使用 `requirements.txt` 作为 `Python` 库的要求。

Github 仓库中的 `Settings` > `Pages` > `Build and deployment` > `source` 中，配置为 `Github Actions` 。

> 最佳实践：在[官方的仓库中](https://github.com/getpelican/pelican/blob/main/.github/workflows/github_pages.yml)有社区维护的工作流，或许直接使用这个工作流更好。

## 插件

原生的 Pelican 有一点毛坯房的意思，需要一些插件来达成目标。

由于插件维护力度等原因，目前的插件都是直接复制到仓库内独立维护，都有不少修订。

### 自动为Pelican标记链接中的相对路径 - auto_attach

基于 [GiovanH的auto_attach插件](https://github.com/GiovanH/peliplugins/blob/master/auto_attach.py) 进行修订。

用于支持相对路径功能，编写文档中的链接时可以直接编写相对路径。插件将会自动根据相对路径指向的实际位置的情况来自动标注类型，供 Pelican 使用。

- 如果文件处在配置的 `STATIC` 路径中（在本仓库目前为 `content/assets` 和 `content/images` ），则直接指向该文件，使用 `{static}` 标记。
- 如果文件不在配置的文章根路径中（在本仓库目前为 `content` ），则说明文件需要额外附加到编译结果中，使用 `{attach}` 标记。
- 否则，使用 `{filename}` 标记，说明文件是编译结果中的文件，比如说其他文章。 Pelican 将会将这种链接转换成对应输出的网页。

插件中的一部分实现比较怪异，或许会因为 Python 版本或者 Pelican 更新而失效。

### 自动根据 Git 提交配置文章时间 - filetime_from_git

基于[官方插件](https://github.com/getpelican/pelican-plugins/tree/master/filetime_from_git)进行修订。

我个人觉得文章元数据中手动编写的时间不合适，首先是格式复杂，其次是完全手动想写什么就什么，和实际的时间可能没有联系。

假设要在 Gihtub 上直接编写，这样的时间也很难用。

由于仓库本身使用 Git 管理，因此使用此插件，从 Git 提交的历史记录中直接自动提取对应的时间。

相比官方插件，主要进行如下修订：

- 文件没有被 Git 管理、添加但尚未提交、修改未提交将告警，可配置
    - 本仓库目前开启全部警告
- 修订获取时间的时区

### 多语言子站点支持 - i18n_subsites

基于[官方插件](https://github.com/getpelican/pelican-plugins/blob/master/i18n_subsites)进行修订。

有故障的插件，但是 `Flex` 主题中的中文支持依赖这个插件，所以只能自己修修使用。

修订后，插件可以支持 `Flex` 的**单语言**站点切换到中文站点，也支持**单个页面切换多种语言**，但是不支持**整个站点同时支持多语言切换**。

相比官方插件，主要进行如下修订：

- 解决多语言页面报 `KeyError` 的错误。

### 专题图片 - featured_image

目前直接从[官方仓库](https://github.com/pelican-plugins/featured-image)复制，还没有任何修订。

在文章列表中使用特定的图像作为文章专题图片。

~~目前插件还有故障，无法正确索引到图像的相对路径。必须手动制定元数据的 `Image` 参数才能正常工作。~~

目前使用仓库特定的方法索引图像路径。

- 对于使用 `Image` 元数据的，只能识别出放在 `CONTENT` 内的 `STATIC` 路径（不需要额外附加 `{static}` 标注）。
- 对于索引文章中图像的，直接用和文章中一致的路径。

### ~~复选框支持 - pelican_md_checklist~~

~~可能由于是 Github 扩展语法， Pelican 默认不支持复选框。需要用插件实现。~~

~~基于 [Markdown 插件](https://github.com/Erik-J-D/florp/blob/main/florp/markdown_checklist.py)，将其改造为 Pelican 插件使用。~~

~~原计划基于 [PIP 仓库中的版本](https://github.com/FND/markdown-checklist/tree/master)支持，但是存在多级情况下的[故障](https://github.com/FND/markdown-checklist/issues/15)。~~

### Markdown 专门的插件支持

直接安装 `pymdown-extensions` ，然后在 `pelicanconf.py` 中启用 `pymdownx.tilde`。

顺便直接启用了 `pymdownx.tasklist` ， 这下完全用不着自定义插件的复选框支持了。 ~~苦~~

后续也许需要同步一些其他插件，参考[这里的配置](https://facelessuser.github.io/pymdown-extensions/faq/#github-ish-configurations)。

另外，将文本高亮中的代码猜测关闭，这个猜测对中文太不友好了。

### 纯文本概要 - plain_text_summary

自己参考和概要相关的插件，自己写了一个对应的插件。

插件的功能，直接删除所有文本格式和图像，只保留文本。

我也不知道 `Pelican` 到底哪里又出毛病了，实现这个比我想象中还麻烦，只能说目前插件能跑。

## 主题

使用 `Flex` 主题，配置简体中文环境。

还没有进一步的定制，或许后面会手动定制一些内容。

## 本地编译

本地使用 `Python3.10.12` 编译。先安装 `virtualenv`。

```
pip install virtualenv
```

然后找一个仓库外的路径，创建虚拟环境。以当前路径为仓库根目录为例，创建到根目录上级的`pelican-venv`中。并引用改环境

```
virtualenv ../pelican-venv
source ../pelican-venv/bin/activate
```

执行后，当前的 `shell` 最前面会多一个 `(pelican-venv)` 提示，代表进入对应的虚拟环境。

安装所有的依赖。

```
pip install -r requirements.txt
```

如果你安装了别的插件，需要依赖，则使用

```
pip freeze > requirements.txt
```

将依赖记录下来，供自动构建使用。

以后就不需要重复上述的操作，直接执行 `source ../pelican-venv/bin/activate` 即可。

直接执行 `pelican -d` 编译。编译结果在 `output` 目录中。

如果编译过程有故障需要调试，使用 `pelican -D` 命令。

如果需要观看编译输出结果，使用 `pelican -l` 命令，将会创建一个临时的本地 http 服务器。用浏览器访问预览。

## 文章

### 在Github编写文章

在 Github 的网页版，可以通过在 `content` 目录中的子目录（该子目录的名称直接作为文章的分类名）直接点击 `Add file -> Create new file` 的方式创建 Markdown 文件，然后直接编写。

也可以在 `content/images` 目录中点击 `Add file -> Upload files` 的方式上传相关的图像。供引用。

### 在本地编写文章

本地使用 `VS Code` 直接编写，搭配 `GitHub Markdown Preview` 实时观看和 Github 一致的预览。

图像文件则放入 `content/images` 中。

如果编写无误，则使用 `git` 将文章和图像一起提交。

### 编写内容

按照一般的 Markdown 写法进行，唯一的区别是需要在开头指定如下元数据：

```
Title: 标题
Tags: 标签1, 标签2
Slug: title-slug
Lang: en
Summary: 摘要
Image: 专题图片路径
```

只有 `Title` 是必选项，理论上 Pelican 可以配置为 `Title` 也可选，不过我还是留着。其他的看情况配置。

### 预览文章

在 Github 仓库中可以直接预览文章。链接和图像的路径能正确解析。

在本地的 VS Code 预览的文章也能正确解析链接和图像，输入过程还能自动提示相对路径地址。

要查看 Pelican 编译的效果，用 `pelican -l` 命令（见上）。

# 待办

- [x] 使用 Pelican
- [x] Github Pages 构建和部署
    - [ ] 构建优化（？）
    - [ ] 用 CF 加速 （？）
    - [ ] 在 CF 上买个域名 （？）
- [x] 插件
    - [x] filetime_from_git
        - [ ] 修订提交到上游
    - [x] i18n_subsites
        - [ ] 修订提交到上游
        - [ ] 修复或者报告子站点故障
    - [x] auto_attach
        - [ ] 修订提交到上游
    - [ ] ~~pelican_md_checklist~~ 不再需要此插件
        - [ ] ~~修订提交到上游（？）~~
    - [x] featured_image
        - [x] 使用最新版
        - [x] 使用仓库特定的方案修订相对路径问题
        - [ ] 通用的方法来修订相对路径问题
    - [x] plain_text_summary
        - [x] 自动生成的概要，移除文本格式
        - [ ] 提交到上游（？ 感觉代码质量不高）
    - [ ] Markdown 相关插件
        - [x] 修订 Markdown 中代码块的奇怪渲染
        - [ ] 检查某些功能是否需要额外开启
- [x] 主题
    - [ ] 整理边栏
    - [ ] 整理顶栏
    - [ ] 社交媒体图标修订，给微博套一个底色
    - [ ] 缩小标题图，默认的太大了
    - [ ] 关闭边栏强制使用小写
    - [ ] 语言标签用“中文/English”，并且强制顺序
    - [ ] 设置一个主页，而不是文章列表

- [ ] 内容
    - [ ] 编写 GameBoy 编程的内容
    - [ ] 编写 GameBoy 汉化的内容
    - [ ] 整理 OpenDingux 的模拟器内容
    - [ ] 整理 OpenDingux 的系统构建
    - [ ] 迁移知乎上的文章到当前站点
    - [ ] 整理关于页面
