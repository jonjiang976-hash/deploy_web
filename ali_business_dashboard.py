#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
阿里国际业务可视化大屏 - 优化版
性能优化：
1. 简化图表配置，提升加载速度
2. 优化HTML布局，确保所有内容可见
3. 减少不必要的动画效果
4. 改进响应式设计
"""

import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

class BusinessDashboard:
    """业务可视化大屏 - 优化版"""
    
    def __init__(self, data_file="saved_data.xlsx"):
        """初始化仪表盘"""
        self.data = None
        self.data_file = data_file
        self.load_data()
        
        # 国家坐标映射（精简版 - 只保留常见国家）
        self.country_coords = {
            '美国': (-95.7129, 37.0902, 'United States'),
            '英国': (-3.4360, 55.3781, 'United Kingdom'),
            '德国': (10.4515, 51.1657, 'Germany'),
            '法国': (2.2137, 46.2276, 'France'),
            '加拿大': (-106.3468, 56.1304, 'Canada'),
            '澳大利亚': (133.7751, -25.2744, 'Australia'),
            '印度': (78.9629, 20.5937, 'India'),
            '日本': (138.2529, 36.2048, 'Japan'),
            '韩国': (127.7669, 35.9078, 'South Korea'),
            '新加坡': (103.8198, 1.3521, 'Singapore'),
            '马来西亚': (101.9758, 4.2105, 'Malaysia'),
            '泰国': (100.9925, 15.8700, 'Thailand'),
            '越南': (108.2772, 14.0583, 'Vietnam'),
            '印度尼西亚': (113.9213, -0.7893, 'Indonesia'),
            '巴西': (-47.8825, -15.7942, 'Brazil'),
            '墨西哥': (-102.5528, 23.6345, 'Mexico'),
            '阿根廷': (-63.6167, -38.4161, 'Argentina'),
            '智利': (-71.5430, -35.6751, 'Chile'),
            '意大利': (12.5674, 41.8719, 'Italy'),
            '西班牙': (-3.7492, 40.4637, 'Spain'),
            '荷兰': (5.2913, 52.1326, 'Netherlands'),
            '比利时': (4.4699, 50.5039, 'Belgium'),
            '瑞士': (8.2275, 46.8182, 'Switzerland'),
            '瑞典': (18.6435, 60.1282, 'Sweden'),
            '波兰': (19.1451, 51.9194, 'Poland'),
            '俄罗斯': (105.3188, 61.5240, 'Russia'),
            '土耳其': (35.2433, 38.9637, 'Turkey'),
            '阿联酋': (53.8478, 23.4241, 'UAE'),
            '沙特阿拉伯': (45.0792, 23.8859, 'Saudi Arabia'),
            '南非': (22.9375, -30.5595, 'South Africa'),
            '埃及': (30.8025, 26.8206, 'Egypt'),
            '尼日利亚': (8.6753, 9.0820, 'Nigeria'),
            '菲律宾': (121.7740, 12.8797, 'Philippines'),
            '新西兰': (174.8860, -40.9006, 'New Zealand')
        }
    
    def load_data(self):
        """加载数据"""
        if os.path.exists(self.data_file):
            try:
                excel_file = pd.ExcelFile(self.data_file)
                
                if len(excel_file.sheet_names) > 1:
                    dfs = []
                    for sheet in excel_file.sheet_names:
                        df = pd.read_excel(self.data_file, sheet_name=sheet)
                        if not df.empty:
                            dfs.append(df)
                    if dfs:
                        self.data = pd.concat(dfs, ignore_index=True)
                else:
                    self.data = pd.read_excel(self.data_file)
                
                if self.data is not None and not self.data.empty:
                    if '询盘时间' in self.data.columns:
                        self.data['询盘时间'] = pd.to_datetime(self.data['询盘时间'])
                    print(f"[OK] 数据加载成功: {len(self.data)} 条记录")
                else:
                    print("[WARNING] 数据为空")
            except Exception as e:
                print(f"[ERROR] 数据加载失败: {e}")
    
    def create_dashboard(self):
        """创建优化的可视化大屏"""
        if self.data is None or self.data.empty:
            print("[ERROR] 没有数据可显示")
            return
        
        print("[INFO] 开始生成可视化大屏...")
        html_content = self._generate_html()
        
        output_file = './output/business_dashboard.html'
        os.makedirs('./output', exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"[OK] 可视化大屏已生成: {output_file}")
        return output_file
    
    def _generate_html(self):
        """生成优化的HTML页面"""
        
        print("[INFO] 生成图表...")
        # 生成所有图表
        map_fig = self._create_world_map()
        trend_fig = self._create_trend_chart()
        level_pie = self._create_customer_level_pie()
        followup_pie = self._create_followup_pie()
        country_bar = self._create_country_bar()
        product_bar = self._create_product_bar()
        method_pie = self._create_method_pie()
        hour_chart = self._create_hour_chart()
        month_bar = self._create_month_bar()
        
        print("[INFO] 计算关键指标...")
        # 计算关键指标
        total_inquiries = len(self.data)
        total_customers = self.data['客户名称'].nunique() if '客户名称' in self.data.columns else 0
        total_countries = self.data['国家'].nunique() if '国家' in self.data.columns else 0
        total_products = self.data['询价产品'].nunique() if '询价产品' in self.data.columns else 0
        
        # 计算各咨询方式的数量
        if '咨询方式' in self.data.columns:
            inquiry_count = len(self.data[self.data['咨询方式'].str.contains('询盘', case=False, na=False)])
            tm_count = len(self.data[self.data['咨询方式'].str.upper().str.contains('TM', na=False)])
            rfq_count = len(self.data[self.data['咨询方式'].str.upper().str.contains('RFQ', na=False)])
        else:
            inquiry_count = tm_count = rfq_count = 0
        
        # 计算转化率（A级客户占比）
        if '跟进等级' in self.data.columns:
            a_level_count = len(self.data[self.data['跟进等级'] == 'A'])
            conversion_rate = (a_level_count / total_inquiries * 100) if total_inquiries > 0 else 0
        else:
            conversion_rate = 0
        
        # 获取数据时间范围
        if '询盘时间' in self.data.columns:
            date_min = pd.to_datetime(self.data['询盘时间'].min()).strftime('%Y-%m-%d')
            date_max = pd.to_datetime(self.data['询盘时间'].max()).strftime('%Y-%m-%d')
            date_range_text = f"数据时间段: {date_min} 至 {date_max}"
        else:
            date_range_text = f"数据更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        print("[INFO] 转换图表为HTML...")
        # 转换图表为HTML（精简模式）
        map_html = map_fig.to_html(include_plotlyjs=False, div_id='map-chart', config={'displayModeBar': False})
        trend_html = trend_fig.to_html(include_plotlyjs=False, div_id='trend-chart', config={'displayModeBar': False})
        level_html = level_pie.to_html(include_plotlyjs=False, div_id='level-chart', config={'displayModeBar': False})
        followup_html = followup_pie.to_html(include_plotlyjs=False, div_id='followup-chart', config={'displayModeBar': False})
        country_html = country_bar.to_html(include_plotlyjs=False, div_id='country-chart', config={'displayModeBar': False})
        product_html = product_bar.to_html(include_plotlyjs=False, div_id='product-chart', config={'displayModeBar': False})
        method_html = method_pie.to_html(include_plotlyjs=False, div_id='method-chart', config={'displayModeBar': False})
        hour_html = hour_chart.to_html(include_plotlyjs=False, div_id='hour-chart', config={'displayModeBar': False})
        month_html = month_bar.to_html(include_plotlyjs=False, div_id='month-chart', config={'displayModeBar': False})
        
        # 生成优化的HTML
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>阿里国际业务智能可视化大屏</title>
    <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
            color: #ffffff;
            overflow-x: hidden;
            overflow-y: auto;
        }}
        
        .dashboard-container {{
            width: 100%;
            padding: 15px;
            padding-bottom: 50px;
        }}
        
        /* 顶部标题栏 - 优化 */
        .header {{
            text-align: center;
            padding: 20px 0;
            background: linear-gradient(90deg, #0a0e27 0%, #1e3a5f 50%, #0a0e27 100%);
            border-bottom: 2px solid #00d4ff;
            margin-bottom: 20px;
        }}
        
        .header h1 {{
            font-size: 36px;
            font-weight: bold;
            color: #00d4ff;
            letter-spacing: 3px;
        }}
        
        .header .subtitle {{
            font-size: 14px;
            color: #00ff88;
            margin-top: 8px;
            letter-spacing: 2px;
        }}
        
        .header .update-time {{
            font-size: 12px;
            color: #888;
            margin-top: 5px;
        }}
        
        /* KPI卡片区域 - 修复为4列2行 */
        .kpi-container {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .kpi-card {{
            background: linear-gradient(135deg, #1a2332 0%, #2d3e5f 100%);
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            border: 2px solid;
            transition: transform 0.2s ease;
        }}
        
        .kpi-card:hover {{
            transform: translateY(-3px);
        }}
        
        .kpi-card.blue {{ border-color: #00d4ff; }}
        .kpi-card.cyan {{ border-color: #00ffff; }}
        .kpi-card.teal {{ border-color: #20b2aa; }}
        .kpi-card.lightblue {{ border-color: #87ceeb; }}
        .kpi-card.green {{ border-color: #00ff88; }}
        .kpi-card.orange {{ border-color: #ffaa00; }}
        .kpi-card.purple {{ border-color: #ff00ff; }}
        .kpi-card.red {{ border-color: #ff4444; }}
        
        .kpi-icon {{
            font-size: 36px;
            margin-bottom: 10px;
        }}
        
        .kpi-value {{
            font-size: 32px;
            font-weight: bold;
            margin: 10px 0;
        }}
        
        .kpi-card.blue .kpi-value {{ color: #00d4ff; }}
        .kpi-card.cyan .kpi-value {{ color: #00ffff; }}
        .kpi-card.teal .kpi-value {{ color: #20b2aa; }}
        .kpi-card.lightblue .kpi-value {{ color: #87ceeb; }}
        .kpi-card.green .kpi-value {{ color: #00ff88; }}
        .kpi-card.orange .kpi-value {{ color: #ffaa00; }}
        .kpi-card.purple .kpi-value {{ color: #ff00ff; }}
        .kpi-card.red .kpi-value {{ color: #ff4444; }}
        
        .kpi-label {{
            font-size: 16px;
            color: #ffffff;
            font-weight: bold;
            margin-bottom: 3px;
        }}
        
        .kpi-sublabel {{
            font-size: 11px;
            color: #888;
        }}
        
        /* 图表容器 - 优化布局 */
        .charts-container {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .chart-box {{
            background: linear-gradient(135deg, #1a2332 0%, #2d3e5f 100%);
            border-radius: 10px;
            padding: 15px;
            border: 1px solid #00d4ff;
        }}
        
        .chart-box.large {{
            grid-column: span 2;
        }}
        
        .chart-box.xlarge {{
            grid-column: span 3;
        }}
        
        .chart-title {{
            font-size: 16px;
            font-weight: bold;
            color: #00d4ff;
            margin-bottom: 10px;
            text-align: center;
        }}
        
        /* 响应式设计 */
        @media (max-width: 1400px) {{
            .kpi-container {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .charts-container {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .chart-box.xlarge {{
                grid-column: span 2;
            }}
        }}
        
        @media (max-width: 768px) {{
            .kpi-container {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .charts-container {{
                grid-template-columns: 1fr;
            }}
            .chart-box.large, .chart-box.xlarge {{
                grid-column: span 1;
            }}
        }}
    </style>
</head>
<body>
    <div class="dashboard-container">
        <!-- 顶部标题 -->
        <div class="header">
            <h1>🌐 阿里国际业务智能可视化大屏</h1>
            <div class="subtitle">ALI INTERNATIONAL BUSINESS INTELLIGENCE DASHBOARD</div>
            <div class="update-time">{date_range_text}</div>
        </div>
        
        <!-- KPI指标卡片 - 4列2行布局 -->
        <div class="kpi-container">
            <div class="kpi-card blue">
                <div class="kpi-icon">📊</div>
                <div class="kpi-value">{total_inquiries}</div>
                <div class="kpi-label">总询盘数</div>
                <div class="kpi-sublabel">Total Inquiries</div>
            </div>
            
            <div class="kpi-card cyan">
                <div class="kpi-icon">💬</div>
                <div class="kpi-value">{inquiry_count}</div>
                <div class="kpi-label">询盘方式</div>
                <div class="kpi-sublabel">Inquiries</div>
            </div>
            
            <div class="kpi-card teal">
                <div class="kpi-icon">🏪</div>
                <div class="kpi-value">{tm_count}</div>
                <div class="kpi-label">TM旺旺</div>
                <div class="kpi-sublabel">TM</div>
            </div>
            
            <div class="kpi-card lightblue">
                <div class="kpi-icon">📝</div>
                <div class="kpi-value">{rfq_count}</div>
                <div class="kpi-label">RFQ报价</div>
                <div class="kpi-sublabel">RFQ</div>
            </div>
            
            <div class="kpi-card green">
                <div class="kpi-icon">👥</div>
                <div class="kpi-value">{total_customers}</div>
                <div class="kpi-label">总访客数</div>
                <div class="kpi-sublabel">Total Visitors</div>
            </div>
            
            <div class="kpi-card orange">
                <div class="kpi-icon">🌍</div>
                <div class="kpi-value">{total_countries}</div>
                <div class="kpi-label">覆盖国家</div>
                <div class="kpi-sublabel">Countries</div>
            </div>
            
            <div class="kpi-card purple">
                <div class="kpi-icon">📦</div>
                <div class="kpi-value">{total_products}</div>
                <div class="kpi-label">产品种类</div>
                <div class="kpi-sublabel">Products</div>
            </div>
            
            <div class="kpi-card red">
                <div class="kpi-icon">🎯</div>
                <div class="kpi-value">{conversion_rate:.1f}%</div>
                <div class="kpi-label">A级转化率</div>
                <div class="kpi-sublabel">Conversion</div>
            </div>
        </div>
        
        <!-- 图表区域 -->
        <div class="charts-container">
            <!-- 世界地图 -->
            <div class="chart-box xlarge">
                <div class="chart-title">🌍 全球客户分布</div>
                {map_html}
            </div>
            
            <!-- 询盘趋势 -->
            <div class="chart-box large">
                <div class="chart-title">📈 询盘趋势分析</div>
                {trend_html}
            </div>
            
            <!-- 客户层级 -->
            <div class="chart-box">
                <div class="chart-title">💎 客户层级分布</div>
                {level_html}
            </div>
            
            <!-- 跟进等级 -->
            <div class="chart-box">
                <div class="chart-title">⚡ 跟进等级分布</div>
                {followup_html}
            </div>
            
            <!-- 国家TOP10 -->
            <div class="chart-box large">
                <div class="chart-title">🌎 TOP10 国家分布</div>
                {country_html}
            </div>
            
            <!-- 产品TOP10 -->
            <div class="chart-box large">
                <div class="chart-title">🔥 TOP10 热门产品</div>
                {product_html}
            </div>
            
            <!-- 咨询方式 -->
            <div class="chart-box">
                <div class="chart-title">📱 咨询方式分布</div>
                {method_html}
            </div>
            
            <!-- 时段分析 -->
            <div class="chart-box">
                <div class="chart-title">⏰ 24小时时段分析</div>
                {hour_html}
            </div>
            
            <!-- 月度对比 -->
            <div class="chart-box">
                <div class="chart-title">📊 月度询盘对比</div>
                {month_html}
            </div>
        </div>
    </div>
</body>
</html>'''
        return html
    
    def _create_world_map(self):
        """创建世界地图 - 性能优化版"""
        if '国家' not in self.data.columns:
            return go.Figure()
        
        country_counts = self.data['国家'].value_counts().head(20)  # 只显示TOP20
        
        lons, lats, sizes, texts = [], [], [], []
        for country, count in country_counts.items():
            if country in self.country_coords:
                lon, lat, en_name = self.country_coords[country]
                lons.append(lon)
                lats.append(lat)
                sizes.append(count)
                texts.append(f"{country}<br>{count}条")
        
        fig = go.Figure(go.Scattergeo(
            lon=lons,
            lat=lats,
            text=texts,
            mode='markers+text',
            marker=dict(
                size=[min(50, max(10, s*2)) for s in sizes],
                color=sizes,
                colorscale='Viridis',
                showscale=True,
                line=dict(width=1, color='white'),
                colorbar=dict(title='询盘数', thickness=10)
            ),
            textfont=dict(size=9, color='white')
        ))
        
        fig.update_layout(
            height=450,
            geo=dict(
                projection_type='natural earth',
                showland=True,
                landcolor='#1e2a3a',
                showocean=True,
                oceancolor='#0d1117',
                bgcolor='#0a0e27'
            ),
            paper_bgcolor='#0a0e27',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        return fig
    
    def _create_trend_chart(self):
        """创建询盘趋势图 - 性能优化版"""
        if '询盘时间' not in self.data.columns:
            return go.Figure()
        
        daily_data = self.data.groupby(self.data['询盘时间'].dt.date).size().sort_index()
        
        fig = go.Figure(go.Scatter(
            x=list(daily_data.index),
            y=list(daily_data.values),
            mode='lines+markers',
            line=dict(color='#00ff88', width=2),
            marker=dict(size=5),
            fill='tozeroy',
            fillcolor='rgba(0, 255, 136, 0.2)'
        ))
        
        fig.update_layout(
            height=350,
            xaxis=dict(showgrid=True, gridcolor='#2d3e5f'),
            yaxis=dict(showgrid=True, gridcolor='#2d3e5f'),
            paper_bgcolor='#1a2332',
            plot_bgcolor='#141b3d',
            font=dict(color='#ffffff'),
            margin=dict(l=40, r=20, t=20, b=40),
            showlegend=False
        )
        return fig
    
    def _create_customer_level_pie(self):
        """创建客户层级饼图"""
        if '客户层级' not in self.data.columns:
            return go.Figure()
        
        level_counts = self.data['客户层级'].value_counts()
        fig = go.Figure(go.Pie(
            labels=list(level_counts.index),
            values=list(level_counts.values),
            hole=0.4,
            marker=dict(colors=['#00d4ff', '#00ff88', '#ffaa00', '#ff00ff'])
        ))
        
        fig.update_layout(
            height=300,
            paper_bgcolor='#1a2332',
            font=dict(color='#ffffff'),
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True
        )
        return fig
    
    def _create_followup_pie(self):
        """创建跟进等级饼图"""
        if '跟进等级' not in self.data.columns:
            return go.Figure()
        
        followup_counts = self.data['跟进等级'].value_counts()
        fig = go.Figure(go.Pie(
            labels=list(followup_counts.index),
            values=list(followup_counts.values),
            hole=0.4,
            marker=dict(colors=['#ff4444', '#ffaa00', '#00ff88', '#888888'])
        ))
        
        fig.update_layout(
            height=300,
            paper_bgcolor='#1a2332',
            font=dict(color='#ffffff'),
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True
        )
        return fig
    
    def _create_country_bar(self):
        """创建国家TOP10柱状图"""
        if '国家' not in self.data.columns:
            return go.Figure()
        
        country_counts = self.data['国家'].value_counts().head(10)
        fig = go.Figure(go.Bar(
            x=list(country_counts.index),
            y=list(country_counts.values),
            marker=dict(color='#00d4ff'),
            text=list(country_counts.values),
            textposition='outside'
        ))
        
        fig.update_layout(
            height=350,
            xaxis=dict(showgrid=False, color='#ffffff'),
            yaxis=dict(showgrid=True, gridcolor='#2d3e5f', color='#ffffff'),
            paper_bgcolor='#1a2332',
            plot_bgcolor='#141b3d',
            font=dict(color='#ffffff'),
            margin=dict(l=40, r=20, t=20, b=60),
            showlegend=False
        )
        return fig
    
    def _create_product_bar(self):
        """创建产品TOP10柱状图"""
        if '询价产品' not in self.data.columns:
            return go.Figure()
        
        product_counts = self.data['询价产品'].value_counts().head(10)
        fig = go.Figure(go.Bar(
            x=list(product_counts.values),
            y=list(product_counts.index),
            orientation='h',
            marker=dict(color='#ff00ff'),
            text=list(product_counts.values),
            textposition='outside'
        ))
        
        fig.update_layout(
            height=350,
            xaxis=dict(showgrid=True, gridcolor='#2d3e5f', color='#ffffff'),
            yaxis=dict(showgrid=False, color='#ffffff'),
            paper_bgcolor='#1a2332',
            plot_bgcolor='#141b3d',
            font=dict(color='#ffffff'),
            margin=dict(l=120, r=40, t=20, b=40),
            showlegend=False
        )
        return fig
    
    def _create_method_pie(self):
        """创建咨询方式饼图"""
        if '咨询方式' not in self.data.columns:
            return go.Figure()
        
        method_counts = self.data['咨询方式'].value_counts()
        fig = go.Figure(go.Pie(
            labels=list(method_counts.index),
            values=list(method_counts.values),
            hole=0.4,
            marker=dict(colors=['#00d4ff', '#00ff88', '#ffaa00', '#ff00ff', '#ff4444'])
        ))
        
        fig.update_layout(
            height=300,
            paper_bgcolor='#1a2332',
            font=dict(color='#ffffff'),
            margin=dict(l=20, r=20, t=20, b=20),
            showlegend=True
        )
        return fig
    
    def _create_hour_chart(self):
        """创建24小时时段分析"""
        if '询盘时间' not in self.data.columns:
            return go.Figure()
        
        hour_counts = self.data['询盘时间'].dt.hour.value_counts().sort_index()
        fig = go.Figure(go.Scatter(
            x=list(hour_counts.index),
            y=list(hour_counts.values),
            mode='lines+markers',
            line=dict(color='#00ff88', width=2),
            marker=dict(size=8, color='#ffaa00'),
            fill='tozeroy',
            fillcolor='rgba(0, 255, 136, 0.2)'
        ))
        
        fig.update_layout(
            height=300,
            xaxis=dict(title='时段', showgrid=True, gridcolor='#2d3e5f', dtick=2),
            yaxis=dict(title='询盘数', showgrid=True, gridcolor='#2d3e5f'),
            paper_bgcolor='#1a2332',
            plot_bgcolor='#141b3d',
            font=dict(color='#ffffff'),
            margin=dict(l=40, r=20, t=20, b=40),
            showlegend=False
        )
        return fig
    
    def _create_month_bar(self):
        """创建月度对比柱状图"""
        if '询盘时间' not in self.data.columns:
            return go.Figure()
        
        month_counts = self.data['询盘时间'].dt.to_period('M').value_counts().sort_index()
        fig = go.Figure(go.Bar(
            x=[str(m) for m in month_counts.index],
            y=list(month_counts.values),
            marker=dict(color=list(month_counts.values), colorscale='Viridis'),
            text=list(month_counts.values),
            textposition='outside'
        ))
        
        fig.update_layout(
            height=300,
            xaxis=dict(title='月份', showgrid=False, color='#ffffff'),
            yaxis=dict(title='询盘数', showgrid=True, gridcolor='#2d3e5f', color='#ffffff'),
            paper_bgcolor='#1a2332',
            plot_bgcolor='#141b3d',
            font=dict(color='#ffffff'),
            margin=dict(l=40, r=20, t=20, b=40),
            showlegend=False
        )
        return fig

if __name__ == "__main__":
    print("=" * 60)
    print("[INFO] 启动阿里国际业务可视化大屏")
    print("=" * 60)
    
    dashboard = BusinessDashboard()
    dashboard.create_dashboard()
    
    print("\n[OK] 可视化大屏已在浏览器中打开！")















