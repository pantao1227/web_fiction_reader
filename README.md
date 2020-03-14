# 小说网站阅读器

这个`Python`脚本用于阅读一些<sup><sub><i>盗版 </i></sub></sup>网站上的小说。

结合Quicker这个工具软件，可以在浏览器的地址栏快速打开脚本。

## 一些小技巧：
QTextEdit使用的HTML的样式是通过`res/style.css`来描述的。其中的`font-family`不能使用中文，例如，“方正聚珍新仿简体”这个字体如果直接写中文名称，就会出错（然而，Chrome 按`F12`检查里直接使用中文是没有问题的）。因此，需要得到字体对应的英文名字。在 Linux 里有个命令是`fc-list`，由于我安装了`texlive`，这个命令在Windows里也是可用的。

先切换Windows控制台编码：

``` batch
chcp 65001
```

列举字体并查找：

``` batch
fc-list | find "FZJ"
```

输出：
``` batch
C:/Windows/fonts/FZJuZXFJW.TTF: FZJuZhenXinFangS\-R\-GB,方正聚珍新仿简体:style=Regular
```

可以得到`FZJuZhenXinFangS\-R\-GB`就是“方正聚珍新仿简体”对应的英文名称。