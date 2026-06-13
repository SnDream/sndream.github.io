---
Title: WSL使用Docker或者coder-server
Slug: wsl-run-docker-and-coder-server
---

只是简单提一下。

对于在 `WSL` 使用 `Docker` 或者 `coder-server` （一个通过浏览器使用`VS Code`的方案） 之类的教程，总是会让你启用 `Systemd` 。

但是，真的有必要吗？如果你不是重度使用者，只是想在需要的时候临时启动一下这些服务使用。平时不需要这些东西持续占用服务的话，根本不需要 `Systemd` 。

至少我目前是这样的。 `Systemd` 在WSL中没有启用。要使用 `Docker` 或者 `Coder-Server`。
直接一个窗口执行 `sudo dockerd` 或者 `coder-server` ，然后该干嘛就干嘛吧。

用完之后，直接在对应窗口 `CTRL+C` 结束守护进程。回收资源。
