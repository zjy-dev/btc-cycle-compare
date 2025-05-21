# btc_cycles_plot.py

import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

# 设置静态图片输出的默认尺寸
pio.kaleido.scope.default_width = 1200
pio.kaleido.scope.default_height = 800

# 下载BTC月线数据
btc = yf.download("BTC-USD", interval="1mo", start="2011-01-01")

# 处理多级列名
btc.columns = btc.columns.droplevel(1)  # 移除多余的列级别
btc = btc.reset_index()

# 重命名列以去除特殊字符
btc = btc.rename(columns={
    'Date': 'Date',
    'Open': 'Open',
    'High': 'High',
    'Low': 'Low',
    'Close': 'Close',
    'Volume': 'Volume'
})

print(f"处理后的数据列: {btc.columns.tolist()}")
print(f"数据前5行:\n{btc.head()}")

# 确保日期列是datetime类型
btc['Date'] = pd.to_datetime(btc['Date'])
btc["YearMonth"] = btc["Date"].dt.to_period("M").astype(str)
print(f"处理后的数据形状: {btc.shape}")

# 打印数据范围用于调试
# print("数据时间范围:", btc['Date'].min(), "到", btc['Date'].max())
# print("可用的年月:", sorted(btc['YearMonth'].unique().tolist()))

# 标记减半 & 顶部
halvings = ["2016-07", "2020-05", "2024-04"]  # 三个完整的减半周期
tops = ["2017-12", "2021-11"]  # 对应的顶部（2025年3月是最近的高点）

btc["Highlight"] = "None"
btc.loc[btc["YearMonth"].isin(halvings), "Highlight"] = "减半"
btc.loc[btc["YearMonth"].isin(tops), "Highlight"] = "周期高点"

# 这里定义固定年份的周期，而不是依据减半日
def get_cycle_by_date_range(start_ym, end_ym, name):
    start_mask = btc["YearMonth"] >= start_ym
    end_mask = btc["YearMonth"] <= end_ym
    cycle = btc[start_mask & end_mask].copy()
    
    if len(cycle) == 0:
        print(f"警告: 没有找到{start_ym}到{end_ym}的数据")
        return None
    
    # 创建月度序号，从1.5开始，右移0.5单位使首月K线完整显示
    cycle["CycleMonth"] = [i + 0.5 for i in range(1, len(cycle) + 1)]
    
    # 先设置周期名称
    cycle["CycleName"] = name
    
    # 然后创建悬浮文本
    cycle["HoverText"] = cycle.apply(
        lambda row: f'{row["YearMonth"]} - {row["CycleName"]}\n'
                   f'开盘: {row["Open"]:.2f}, 收盘: {row["Close"]:.2f}\n'
                   f'最高: {row["High"]:.2f}, 最低: {row["Low"]:.2f}', 
        axis=1
    )
    return cycle

# 每个周期使用固定年度的数据
cycle1 = get_cycle_by_date_range("2016-01", "2019-12", "2016-2019周期")
cycle2 = get_cycle_by_date_range("2020-01", "2023-12", "2020-2023周期")
cycle3 = get_cycle_by_date_range("2024-01", "2025-05", "2024-2025当前周期")

# 合并
all_cycles = pd.concat([cycle1, cycle2, cycle3])

# 画蜡烛图函数
def make_candles(cycle_df, color):
    # 确保数据按日期排序
    cycle_df = cycle_df.sort_values('Date')
    
    return go.Candlestick(
        x=cycle_df["CycleMonth"],
        open=cycle_df["Open"],
        high=cycle_df["High"],
        low=cycle_df["Low"],
        close=cycle_df["Close"],
        name=cycle_df["CycleName"].iloc[0],
        increasing_line_color=color,
        decreasing_line_color=color,
        text=cycle_df["HoverText"],   # 使用自定义的悬浮文本
        hoverinfo='text',            # 显示自定义文本
        showlegend=True,
        xaxis='x',
        yaxis='y',
        visible=True
    )

# 高亮点
def highlight_points(cycle, label, color):
    highlights = cycle[cycle["Highlight"] == label]
    hover_texts = []
    for _, row in highlights.iterrows():
        hover_text = f'{row["YearMonth"]} - {label}\n'\
                    f'{row["CycleName"]}\n'\
                    f'价格: {row["High"]:.2f}'
        hover_texts.append(hover_text)
    
    # 只在第一次调用时显示图例
    show_legend = not hasattr(highlight_points, 'legend_shown')
    if show_legend:
        highlight_points.legend_shown = True
    
    return go.Scatter(
        x=highlights["CycleMonth"],
        y=highlights["High"],
        mode="markers+text",
        text=[label] * len(highlights),
        textposition="top center",
        hovertext=hover_texts,  # 自定义的悬浮文本
        hoverinfo="text",       # 显示自定义文本
        marker=dict(size=10, color=color),
        name=label,
        # name=f"{cycle['CycleName'].iloc[0]} - {label}"

        #    mode="markers",
        # marker=dict(color=color, size=10, line=dict(width=1, color='black')),
        # name=label,
        # text=hover_texts,
        # hovertext=hover_texts,
        # hoverinfo="text",
        # hovertemplate='%{text}<extra></extra>',
        #  showlegend=show_legend
    )

# 创建图
fig = go.Figure()

# 为每个周期创建蜡烛图
colors = ["#1f77b4", "#2ca02c", "#ff7f0e"]  # 蓝色、绿色、橙色
cycles = [cycle1, cycle2, cycle3]
cycle_names = ["2016年减半周期", "2020年减半周期", "2024年减半周期"]

# 添加所有周期的K线图
for i, (cycle, color, name) in enumerate(zip(cycles, colors, cycle_names)):
    # 添加蜡烛图
    fig.add_trace(make_candles(cycle, color))

# 只添加一次高亮点的图例
for i, (cycle, color, name) in enumerate(zip(cycles, colors, cycle_names)):
    # 只在第一个周期添加图例，其他周期不显示图例
    show_legend = (i == 0)
    
    # 添加高亮点 - 减半
    highlight = highlight_points(cycle, "减半", "yellow")
    highlight.showlegend = show_legend
    fig.add_trace(highlight)
    
    # 添加高亮点 - 顶部
    top = highlight_points(cycle, "周期高点", "red")
    top.showlegend = show_legend
    fig.add_trace(top)

# 设置浅色主题与图表属性
fig.update_layout(
    title={
        'text': "比特币周期对比（按年份划分）",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis_title="周期月数",
    yaxis_title="BTC 价格（USD）",
    template="plotly_white",  # 切换为浅色主题
    xaxis=dict(
        tickmode="linear",
        showgrid=True,
        zeroline=True,
        rangeslider=dict(visible=False),  # 禁用范围滑块
        range=[1, 50]  # 设置坐标范围，去除负数
    ),
    yaxis=dict(
        type="log",  # 使用对数坐标轴，因为BTC价格范围很大
        showgrid=True,
        zeroline=True,
        gridcolor='rgba(200,200,200,0.2)'  # 浅色网格
    ),
    legend=dict(
        bgcolor='rgba(255,255,255,0.5)',
        bordercolor='rgba(0,0,0,0.1)',
        borderwidth=1
    ),
    plot_bgcolor='rgba(255,255,255,1)',  # 图表背景
    paper_bgcolor='rgba(255,255,255,1)',  # 纸张背景
    showlegend=True,
    hovermode='x unified'
)

# 保存为HTML文件
output_html = "btc_cycles_comparison.html"
fig.write_html(output_html)
print(f"交互式图表已保存为: {output_html}")
    