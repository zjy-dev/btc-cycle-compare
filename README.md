# 📈 比特币减半周期比较工具

![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

🔍 这个项目用于分析和可视化比特币（BTC）在历史减半周期中的价格表现。通过对比不同减半周期，帮助投资者更好地理解比特币的市场行为。

## ✨ 功能特点

- 📊 可视化比特币减半周期的价格走势
- 🎨 支持交互式图表（HTML）和静态图片（PNG/JPG/SVG/PDF）导出
- 🔍 标记重要事件点：减半事件和周期高点
- 📈 多周期对比分析
- 🖱️ 悬停显示详细信息

## 🚀 快速开始

### 安装依赖

```bash
# 使用 uv 安装依赖
uv pip install -r requirements.txt
```

### 运行程序

```bash
python btc_cycles_plot.py
```

运行后将在当前目录下生成以下文件：
- `btc_cycles_comparison.html` - 交互式HTML图表
- `btc_cycles_comparison.png` - PNG格式图片
- `btc_cycles_comparison.jpg` - JPG格式图片
- `btc_cycles_comparison.svg` - SVG矢量图
- `btc_cycles_comparison.pdf` - PDF文档

## 📊 图表说明

- 每个减半周期用不同颜色的K线图表示
- 🔴 红色圆点标记减半事件（Halving）
- 🟡 黄色圆点标记周期高点（Top）
- 悬停在数据点上可查看详细信息

## 🛠️ 自定义设置

您可以在 `btc_cycles_plot.py` 中修改以下参数来自定义图表：

- `halvings` - 减半事件的年月列表
- `tops` - 周期高点的年月列表
- 图表标题、尺寸等参数

## 📝 依赖项

- Python 3.7+
- pandas
- yfinance
- plotly
- kaleido (用于导出静态图片)

## 📄 许可证

本项目采用 [MIT](LICENSE) 许可证

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📬 联系

如有任何问题或建议，请随时联系项目维护者。

---

<div align="center">
  Made with ❤️  by BTC 爱好者
</div>
