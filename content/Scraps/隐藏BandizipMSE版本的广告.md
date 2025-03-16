---
Title: 隐藏 Bandizip MSE 版本的广告
Slug: bandzip-mse-hide-ad
---

# BandizipMSE-HideAD

代码仓库：[BandizipMSE-HideAD](https://github.com/SnDream/BandizipMSE-HideAD)

> 本文仅作为记录，本文后续正常只更新 [仓库中的Readme](https://github.com/SnDream/BandizipMSE-HideAD)

使用非侵入式（存疑，因为目前引入了一个程序）的方法隐藏 Bandizip MSE 版本 (Microsoft Store) 右下角的弹出广告。

# 原理

Bandizip 可以通过导入reg配置的方式更新配置。

Bandizip 每日仅显示一次广告。通过计划任务，每日将当天的日期作为 Bandizip 已经显示过广告的日期的相关配置，合并到 reg 配置。

由于 Bandizip 目前必须在初始化状态下才能导入 reg 配置，因此计划任务还会将 Bandizip 的软件配置重置。

# 优点

1. 不再看到右下角弹出的广告。
2. 没有对原始软件进行任何修改。

# 缺陷

1. 由于软件配置会被重置，无法记录历史曾经打开的文件。
2. 进程配置会每日被复位为最后一次导入 reg 配置的状态。
    1. 修改配置还是可以的，但是会变得复杂，见下文。
3. 为了实现后台无感运行脚本，引入了一个程序。

# 使用方法

1. 打开 `Bandizip`，按照你的需要修改 Bandzip 的配置。
2. 选择 `选项` - `设置` - `高级` - `导出 Bandizip 设置`，并保存导出的 `.reg` 文件。
3. 关闭 `Bandizip`，打开 `.reg` 文件，进行 reg 配置的导入。
    1. 如果遇到 `更改系统` 或者 `注册表编辑器` 的提示，请选择 `是` 确认。
4. 从 [这里](https://github.com/SeidChr/RunHiddenConsole/releases) 下载 `hiddenw.exe` ，用于进程的后台执行。
5. 下载后，将 `hiddenw.exe` 重命名为 `powershellw.exe` ，并放入 `C:\Windows\System32\WindowsPowerShell\v1.0` 路径。
    1. 放好后，执行一次，如果Windows提示未知来源，允许执行。
    2. 没办法，目前 Windows 似乎没有什么正经的后台运行脚本的方式。
6. 下载 `Reset Bandizip - UserLess.xml`
7. 打开 `cmd` （命令提示符） 窗口，输入 `whoami /user`
    1. 打开的窗口中会提示你的 `SID`
    2. 格式类似于 `S-1-5-21-0123456789-9876543210-123456789-1001`
    3. 下文以此SID为例子，你应该使用你对应的SID。
8. 用 `记事本` 打开第6步的 `.xml` 文件，将文件中的 `S-1-5-21-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXX-1001` 替换成你第7步中获取的 `SID`
    1. 替换后的格式类似于 `<UserId>S-1-5-21-0123456789-9876543210-123456789-1001</UserId>`
    2. 替换完成后，保存文件。
9.  打开 `任务计划程序` , 点击 `导入任务` ，选择修改好的 `.xml` 文件。
    1. 出来的窗口中的 `运行任务时，请使用下列用户账户` ，应该为你的具体用户名，而**不是** `S-1-5-21-XXXXXXXXXX-XXXXXXXXXX-XXXXXXXXX-1001`
    2. 如果不能正常显示用户名，请手动使用 `更改用户或组` 修改
10. 之后，就可以使用没有广告的 `Bandizip`

# 如何修改配置

后续如果需要修改 `Bandizip` 的配置，请重新操作 `使用方法` 的前3步内容，将最新配置对应的 `.reg` 导入，否则配置会复位为最后一次 `.reg` 导入时的状态。

# Bandizip 已经更新了，用不了这个方法了，怎么办？

目前(2025.03.07)在 `Bandizip 7.37` 上支持，不确定后续版本是否还能支持，因为官方可以轻易禁止此方法，能用一天算一天吧。

非侵入式的方法局限性很大，唯一的优点是没有对原始程序进行任何修改。

如果软件更新，此方法不再可用，我也没有办法。

如果你能接受 `微软电脑管家` ，可以直接使用内置功能隐藏广告。如果不能接受，更换成 `Nanazip / 7-zip` （如果你没有钱）。

或者，购买 `Bandizip` 的个人版（如果你有钱）。
