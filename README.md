# Kokomi_bot 部署教程 (V 5.0.0+)

> 当前教程为 v5 版本，如需查看 v4 版本的教程，请点击[此处](https://github.com/SangonomiyaKoko/Kokomi_Bot/blob/main/README_OLD.md)

## V5 版本 bot 尚在开发中，请耐性等待

## 环境搭建

```bash
git clone https://github.com/SangonomiyaKoko/Kokomi_Bot.git  # 下载代码

python -m venv .venv  # 创建虚拟环境

.venv/Scripts/activate  # 激活虚拟环境

pip install -r requirements.txt # 安装python依赖
```

注意，如果使用了虚拟环境，请务必确保后续的依赖安装和程序运行都在虚拟环境内

如果你是程序小白不清楚的话，不使用虚拟环境也是可以的

## 下载静态图片资源

此处后续为自动更新，目前未完成开发如有需要请联系开发者

## 配置 env

在项目文件内有一个 `.env.example` 的示例文件，复制并重名为 `.env`

然后按照自己的需求修改配置项目

## 启动测试

运行 test.py 文件，输入指令能够成功生成图片则说明运行成功
