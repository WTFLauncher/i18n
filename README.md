# WTFLauncher 翻译源

WTF Launcher 的启动器界面翻译仓库，供启动器在运行时下载语言包使用。产出站点：
https://wtflauncher.github.io/i18n/ ，启动器读取的入口是其中的 index_v2.json 。

本仓库是 [PrismLauncher/Translations](https://github.com/PrismLauncher/Translations) 的 fork，
翻译内容本身由 [Hosted Weblate](https://hosted.weblate.org/projects/prismlauncher/launcher/) 维护，
授权为 Apache License 2.0，见 LICENSE 。

## 与上游的差异

- 构建脚本允许单个语言的 msgfmt 校验失败，只记录统计数字而不中断整批构建，一门语言有问题不会让其余一百种语言发不出去。
- 没有 .github/CNAME ，站点由 GitHub Pages 的项目地址提供。
- update.yml 已停用，因为它需要上游的 weblate 凭据。同步上游改动请使用 git merge 或仓库页面上的 Sync fork 。

## 目录与产物

仓库里是各语言的 .ts 文件（Qt 翻译源格式）。构建流程为：每个 .ts 先用 lconvert 转出 .po 以便统计，
再用 lrelease 编译成 .qm，然后以该 .qm 自身的 sha1 作为文件名复制一份并加上 .class 后缀，
同时写出 index_v2.json 记录每种语言的文件名、sha1、大小与已译、模糊、未译数量。

启动器会校验下载文件的 sha1，所以文件名与索引必须一致。

## 本地重建

安装 Qt 的 lconvert 、 lrelease 、lupdate 与 gettext 的 msgfmt 后执行：

    nix develop . -c ./release.sh

或者不用 nix，直接：

    ./release.sh

产物出现在 build 目录。日常发布不需要本地跑，推送 .ts 改动会触发 Build Pages 工作流自动发布。
