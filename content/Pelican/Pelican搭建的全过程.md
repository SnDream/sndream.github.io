Title: Pelican搭建的全过程
Tags: Pelican, 过程记录
Slug: pelican-build-process-all
Summary: Pelican的生态比想象中更差一些。

# 前言

几个月前买了云主机，本来想搭建一个简单的站点记录一些 `GameBoy编程` 和 `OpenDingux` 的内容。
结果只过了 ICP 备案，干脆不搞了。打算直接用 `Github Pages` 来搭建静态站点。

加上知乎上写的东西不能被搜索引擎正常抓取到[^zh]，我也在计划将之前写的一些内容迁移到这个站上。

后面再看看要不要买个域名吧，目前先不花这个钱。

# 选择 Pelican

`Github Pages` 的官方静态使用的是 `Jekyll` ，由于我不太想额外装 `Ruby` ，所以不打算用这个。

经过一些简单的选择后，我选择了 `Pelican` 作为建站。
其实没什么原因，就是因为 `Pelican` 使用的是 `Python` ，好歹用过，出问题自己可以修一修（结果一语成谶）。

经过简单的学习，使用 `pip` 安装完 `Pelican` 和 `Markdown` 后，就可以直接执行 `pelican-quickstart` 创建初始化的仓库。然后就开始受难了。

# 元数据

`Pelican` 需要在编写的文档前增加元数据。常见的元数据有这些参数。

```
Title: 标题
Date: 2024-07-07 19:18
Modified: 2024-07-07 19:19
Category: 分类
Tags: 标签1, 标签2
Slug: title-slug
Lang: 语言
Authors: 作者
Summary: 摘要
```

参数 `Title` 虽然按教程是配置成可以省略的，不过我还是写一下。

参数 `Category` `Authors` 可以自动生成，所以不写。

参数 `Slug` 用于网页名的缩写，作为文章的ID，虽然可以自动生成，但是由于有写中文/英文关联的必要，因此我选择手动写。

参数 `Lang` 按官方文档应该每一篇都写的，不过我打算只给英文版本写，其余用默认参数，也就是中文。

参数 `Tags` `Summary` 按需写就可以，想写就写，不写也无所谓。

其他的参数我都能理解，唯独参数 `Date` 和 `Modified` ，首先是 `Date` 必须手动编写，其次是时间这种东西手写实在难受。

既然我的文档是用 `Git` 管理，理论上完全可以用 `Git` 的最早和最晚的提交时间作为文件的 `Date` 和 `Modified` ，于是我询问了一下相关的使用方法，获得了维护者的回复[^pd]。
维护者推荐 `filetime_from_git` ，试用后确实有对应的效果，然而这里也为后续埋了第一个坑。

整理后，写文档前只需要如下元数据：

```
Title: 标题
Tags: 标签1, 标签2
Slug: title-slug
Lang: en
Summary: 摘要
```

# Github Pages 自动部署

本地简单验证后，我开始将内容提交到 [Github仓库](https://github.com/SnDream/sndream.github.io) 里，然后开始现学如何自动部署 `Github Pages`。

这里，我发现了 `Pelican` 的第一个生态问题， 相比于 `Jekyll` 有全套官方支持， `Pelican` 在 `Githbu Actions` 市场上没找到什么好用的部署工作流。

> 附注：实际上官方仓库中是有一个 [社区维护的工作流](https://github.com/getpelican/pelican/blob/main/.github/workflows/) 。
> 从写的配置看感觉还挺全面的，不过我都搭建完了才发现，最终没用这个。

上面的大部分部署方法大概按这个方法进行：

1. 基于 `Python` 的 `Docker` 镜像，进行基本配置
2. 安装 `Pelican` 等相关组件
3. 使用 `Pelican` 构建站点内容
4. 将构建结果提交到当前 `Github` 仓库或者 `gh-pages` 分支。

实际操作中，我没有成功构建，构建的提交被 Github 拦截了，不知道具体原因。
而且这种提交方法我也不喜欢，我不想把编译结果作为 Github 仓库的一部分提交。
于此同时，我在 Github 上看到一些仓库就是这样提交的，甚至有一些就只有编译的结果被提交上来，我觉得这样用 Git 太奇怪了。

实际上， Github 最新的部署方法不需要再提交到仓库里，本身可以直接部署。但是我（当时）没找到相关的方案。

于是我基于 `Jekyll` 的官方构建流程，官方的构建流程是多个步骤进行的，将里面的 `jekyll-build-pages` 开分支出来，将其替换成 `Pelican` 的相关编译环境。其余的内容和 `Jekyll` 的流程保持一致。

经过这么操作后，我的站点终于成功通过编译和部署，部署的坑也一个个冒出来了。

## 第一个坑：时间元数据错误

部署后的页面出现一个问题，所有的文章的时间都是部署的时间，而不是根据 `Git` 提交的时间。

这个时候我才实际看 `Github Action` 的工作流程，其中有一步是 `checkout@v4` ，里面为了性能只会下载最后一次提交，所以所有的文章可能因为这个修订导致所有文章的时间都集中在这个提交上。
因此这里我尝试修改 `checkout@v4` 的参数，结果没有解决问题。

`Github Action` 本身挺麻烦的，由于不是本地环境，只能一次次提交来输出各种调试。经过几天的折腾，终于看到这个输出：

```
fatal: detected dubious ownership in repository at '/github/workspace'
To add an exception for this directory, call:

	git config --global --add safe.directory /github/workspace
```

不知道怎么搞的，可能还是我构建的镜像有问题，下载的流程用的是某个用户进行，但是编译时的用户就是 `root` 了。`git` 在这种场景下会认为当前的仓库归属不正常，可能造成安全因素，因此要求你设置 `safe.dirctory`。

然后，就是下一个巨坑， `filetime_from_git` 对这种情况竟然毫无输出，因此从 `Pelican` 的输出中根本看不到这个问题。 经过一通折腾，我也没办法修改好 `filetime_from_git` ，里面某些直接调用 `git` 命令就会有类似的故障。

最终的修订方案大致如下：

1. 在 `filetime_from_git` 增加警告，对文件未添加过、添加未提交过、非Git仓库中的文件等提供警告。默认关闭。
2. 在构建镜像中配置如下配置，关闭 `safe.directory` 的配置，反正编译过程只需要输出：

```
echo 'Git safe.directory config👷 '
export GIT_CONFIG_COUNT='1'
export GIT_CONFIG_KEY_0='safe.directory'
export GIT_CONFIG_VALUE_0='*'
```

到这里， Github 的每一次提交就能自动构建。由于 Github 可以直接创建和编译新文件，理论上是可以直接在网页写新文件，写完提交 Github 就能自动部署了。

# 选择主题

默认的主题不算好看，因此还是选一个主题，这里算是感觉 `Pelican` 生态有问题的另一个地方。
在[`PelicanThemes`](https://pelicanthemes.com/)上翻了半天。上面的主题给我的感觉就是太老气了。

去仓库一看，确实如此，许多主题都是十年前制作的，也没有更新。最新更新的主题也是基本没有。

最终选择 [`Flex`](https://github.com/alexandrevicenzi/Flex) 主题，这个算是比较现代，实际上也是比较常见的主题，虽然上一次正式也是两年前的事情了。

这一块其实还好，就是正常配置主题，唯一的问题还是没什么可选的主题。

`Flex` 的配置项其实不少，不可配置项也不少，后面可能得自己学习 CSS 等进行更细节的修改，我实在不想将主题也分支后改自己的版本了。

标题图和`favicon.ico` 是直接用生成器生成的，直接用 Emoji🕹️ 在 [Favicon Generator](https://favicon.io/favicon-generator/) 生成[^em]。

对了，我是将主题作为子仓库链接到当前的仓库的。 `Github Pages` 构建中需要把 `checkout@v4` 里的相关配置打开，让他能够递归下载主题仓库。

# 多语言

我计划站点主要还是中文编写，用于记录 `GameBoy编程` 的内容，不过我也计划将之前维护的一些 `OpenDingux` 的模拟器进行整理，这一部分可能需要一个英文页面。

`Flex` 支持对站点配置中文，需要 `i18n_subsites` 插件。这也成为我下一个坑的来源。

## 第二个坑：i18n_subsites 插件的故障

我一开始是计划将网站直接输出为中文和英文两个版本，既然都装了 `i18n_subsites` 插件用于配置主题的语言，这么做不是很自然的么。

但实际上 `i18n_subsites` 一开启，只要你尝试为同一个页面同时创建英文和中文版本，编译过程就会有无穷无尽的故障，怎么折腾都不正常。故障时会打印大概这样的内容：

```
CRITICAL KeyError: translated.md
```

没办法了，只能自己一点点调试，主要的报错内容是某个页面去某个字典中寻找自己的翻译内容时根本找不到对应的字段。代码中只会将当前站点语言的内容加到这个字典。
不知道其他人怎么用的，都没遇到相同问题，我只能自己手动修一修这个插件了。

修完之后，编译会报如下内容：

```
WARNING  There are 2 items "with slug "gbprog"" with lang en:
         sndream.github.io/content/GameBoy/GameBoy编程.md
         sndream.github.io/content/GameBoy/GameBoyProg.md
WARNING  There are 2 original (not translated) items with slug "gbprog":
         sndream.github.io/content/GameBoy/GameBoy编程.md
         sndream.github.io/content/GameBoy/GameBoyProg.md
CRITICAL RuntimeError: File sndream.github.io/output/en/gameboy/gbprog.html is to be overwritten
```

从日志看，内容非常奇怪，明明理论上用`{slug}-{lang}`的组合作为key不应该有这个问题，但是实际编译上就是在报错， `Pelican` 在这个场景认为两篇文章同时是英文，且同时没有翻译。
和中文页面的 `Lang` 没写也没关系，哪怕我每一篇都写也是这个故障。

没辙了，实在不能解决这里面的每一个问题，如果不将两个文章关联那是可以正常生成，但是每个语言版本都会出现一次，而且语言版本之间没有关联。这样还不如不构建专门的英文站。
于是目前就只能关掉英文站的生成，只生成中文站。

作为弥补，也是因为我实际上也不会在这个站点上维护多少英文版本的页面（想想也不会有人看），因此我在边栏单独增加一个英文页面，索引一些相关的信息，也就够了。

# 相对链接

到这里，整个架子其实就差不多了，但是实际开始写内容的时候，新的问题又接踵而至：我如何链接到另一篇文章或者图片。

按照 `Markdown` 的正常写法，相对链接和图片应该这么写：

```
![图片说明](../images/图片.png)
[链接说明](../pages/about.md)
```

但是 `Pelican` 并不能直接识别这样的链接，这就引出了下一个坑。

## 第三个坑：构建相对链接

`Pelican` 里，要求你手动指定相对链接的类型，得这么写：

```
![静态的图片]({static}../images/图片.png)
![非静态图片]({attach}../images/图片.png)
[普通的链接]({filename}../pages/about.md)
```

说实话，这太奇葩了，这样的首要问题是这些链接不被我写 `Markdown` 的 `VS Code` 识别，在 `Github` 上直接看文件也无法正常索引到目标。

我不知道为什么要这么设计，因为 `Pelican` 对我来说也是新手，只能又开始新一轮的搜索。
最终找到一个 [私人仓库](https://github.com/GiovanH/peliplugins) 的 `auto_attach` 插件。

不过他的这个插件主要用于图像的链接，因此他的代码是强制使用 `{attach}` 的，这样用不适合链接放在静态目录中的图像。也不适合链接自动生成的文章。

没办法了，继续修改吧，给 `auto_attach` 插件增加了功能，根据链接的文件路径自动确定要加 `{attach}` `{static}` 还是 `{filename}` 。

- 如果文件在配置的静态目录中，就用 `{static}` 
- 如果文件在配置的 `Pelican` 内容目录中，则使用 `{filename}` 
- 否则，使用 `{attach}` ，将文件主动加入构建结果中。这个理论上不会出现在这个仓库里。

我其实感觉这个应该内置在 `Pelican` 里面，自动识别的，不知道开发者具体怎么想的。

修改之后，文章内部的相对链接可以正确识别，也可以正确编译。整个网站的搭建初步完成了。

# 结尾

到目前，整个站点的架构算是搭起来了。
中间的坑实际上踩了不少，上面写到的基本上都只写了最终方案，但是到达最终方案的路上折腾了不少时间。

这里整理一下，后续还能做什么吧。顺便，为了支持下面的勾选框，还当场引入一个新插件，还需要按 `Pelican` 的用法去修订。

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
    - [x] pelican_md_checklist
        - [ ] 修订提交到上游（？）
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


[^zh]: [如何看待知乎禁止必应和谷歌搜索、抓取其内容](https://www.zhihu.com/question/657376810) .
[^pd]: [Automatic generation of date metadata](https://github.com/getpelican/pelican/discussions/3352) .
[^em]: 实际上摇杆的圆点好像不在图像中心上，不过真有人注意到并且看得不爽吗？
