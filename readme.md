# 摸鱼听书

> WSL 下的听书软件, 后端使用[hectorqin/reader] (https://github.com/hectorqin/reader); 调度使用[yuhldr/heartale](https://github.com/yuhldr/heartale); tts 使用[sherpa-onnx] (https://github.com/k2-fsa/sherpa-onnx)

> 三个模块都使用 docker 启动, 因此需要在 wsl 内安装 docker 并启动三个容器

## 使用

> 拉下代码后, 进入 reader 目录, 执行 `docker compose build` 构建镜像

> 启动三个容器, 执行 `docker compose up -d`


## 配置
> 详见 [yuhldr/heartale](https://github.com/yuhldr/heartale) 的配置说明