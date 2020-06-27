* 安装要求：
```
tensorflow 1.0+
python 2+
all platform
```

* 安装：
```
git clone https://github.com/zhang-li-peng/TensorFlow-Tang-Poems.git
```

* 使用方法：
```
# for poem train
python main.py -w poem --train

# for generate poem
python main.py -w poem --no-train


```

* 参数说明
`-w or --write`: 设置作诗，poem表示诗
`--train`: 训练标识位，首次运行请先train一下...
`--no-train`: 生成标识位
