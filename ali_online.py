#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里国际业务智能复盘工具 - 在线版（Streamlit）
可部署到云端的Web应用：包含导入/预览/筛选/图表/报告/提醒/导出/保存等功能

启动（本地开发）：
  streamlit run ali_online.py --server.port 8501 --server.address 0.0.0.0

部署（云端）建议：
  - 确保安装依赖：streamlit, pandas, pillow, plotly, openpyxl 等
  - 将工作目录设置为项目根目录（可写output/目录）
  - 避免使用任何阻塞式弹窗（全部改为页面提示）
  - PythonAnywhere等平台：确保使用 streamlit run 命令启动
"""

import os
import sys
import io
import json
import time
import pandas as pd
from datetime import datetime, timedelta

# 环境检测：确保在 Streamlit 环境中运行
try:
    import streamlit as st
    # 检测 session_state 是否可用（bare mode 中可能不可用）
    try:
        _ = st.session_state
        STREAMLIT_AVAILABLE = True
    except (RuntimeError, AttributeError) as e:
        # 如果在 bare mode，session_state 不可用
        STREAMLIT_AVAILABLE = False
        STREAMLIT_ERROR = str(e)
except ImportError:
    st = None
    STREAMLIT_AVAILABLE = False
    STREAMLIT_ERROR = "Streamlit 未安装"

# 如果在非 Streamlit 环境中，显示友好错误页面
if not STREAMLIT_AVAILABLE:
    if st is not None:
        # 在 Streamlit 中但 session_state 不可用（bare mode）
        st.set_page_config(page_title="环境错误", layout="centered")
        st.error("""
        # ⚠️ Streamlit 环境配置错误
        
        此应用无法在 bare mode 下运行。Session state 功能不可用。
        
        **解决方案：**
        
        请使用以下命令启动应用：
        ```
        streamlit run ali_online.py
        ```
        
        如果使用 PythonAnywhere，请确保：
        1. 在 Web 应用中配置了 Streamlit
        2. 或者通过 SSH 使用 `streamlit run` 命令启动
        """)
        st.stop()
    else:
        # 完全没有 Streamlit
        print("=" * 60)
        print("错误：此应用必须在 Streamlit 环境中运行！")
        print("=" * 60)
        print()
        print("正确的启动方式：")
        print("  streamlit run ali_online.py")
        print()
        print("如果使用 PythonAnywhere，请使用：")
        print("  streamlit run /path/to/ali_online.py")
        print("=" * 60)
        sys.exit(1)

# 第三方可选依赖（按需导入）
try:
    from PIL import Image
except Exception:
    Image = None

# 初始化错误处理变量
_import_error_message = None

try:
    from ali_business_analyzer import AliBusinessAnalyzer
except Exception as e:
    # 保存错误信息，稍后在Streamlit上下文中显示
    _import_error_message = str(e)
    AliBusinessAnalyzer = None

try:
    from ali_business_dashboard import BusinessDashboard  # 可选
    DASHBOARD_AVAILABLE = True
except Exception:
    DASHBOARD_AVAILABLE = False


# ========== 基础工具 ==========
def get_default_config():
    return {
        "contact_methods": ["tm", "询盘", "WhatsApp", "邮件", "电话", "微信"],
        "handlers": ["Kim", "Alice", "Bob", "Charlie", "David"],
        "customer_levels": ["L0", "L1", "L2", "L3", "L4"],
        "continents": ["亚洲", "欧洲", "北美洲", "南美洲", "非洲", "大洋洲"],
        "follow_up_levels": ["A", "B", "C", "X"],
        "export_settings": {"default_filename": "询盘分析表.xlsx", "date_format": "%Y-%m-%d"}
    }


def ensure_output_dir():
    os.makedirs("output", exist_ok=True)
    os.makedirs(os.path.join("output", "uploads"), exist_ok=True)


def show_import_error():
    """显示导入错误"""
    if _import_error_message:
        st.error(f"无法导入 AliBusinessAnalyzer：{_import_error_message}")
        st.info("""
        **解决方案：**
        1. 确保 `ali_business_analyzer.py` 文件存在
        2. 检查所有依赖是否已安装：`pip install -r requirements_web.txt`
        3. 查看服务器日志获取详细错误信息
        """)
        st.stop()

def init_state():
    """初始化 session state（安全版本）"""
    try:
        if "analyzer" not in st.session_state:
            if AliBusinessAnalyzer is None:
                show_import_error()
            st.session_state.analyzer = AliBusinessAnalyzer()
        if "data" not in st.session_state:
            st.session_state.data = None
        if "filtered_data" not in st.session_state:
            st.session_state.filtered_data = None
        if "monthly_data" not in st.session_state:
            st.session_state.monthly_data = {}
        if "config" not in st.session_state:
            # 优先读取本地 config.json，否则使用默认
            cfg = get_default_config()
            if os.path.exists("config.json"):
                try:
                    with open("config.json", "r", encoding="utf-8") as f:
                        cfg.update(json.load(f))
                except Exception:
                    pass
            st.session_state.config = cfg
    except (RuntimeError, AttributeError) as e:
        # session_state 不可用时，显示错误
        st.error(f"Session state 不可用：{e}")
        st.info("""
        这通常发生在应用没有通过 `streamlit run` 启动时。
        
        请确保使用正确的启动命令：
        ```
        streamlit run ali_online.py
        ```
        """)
        st.stop()


def load_saved_data_silently():
    """静默加载保存的数据"""
    try:
        save_file = "saved_data.xlsx"
        if os.path.exists(save_file):
            st.session_state.analyzer.read_excel(save_file)
            st.session_state.data = st.session_state.analyzer.data
            # 统一将'询盘时间'转换为datetime
            try:
                if st.session_state.data is not None and '询盘时间' in st.session_state.data.columns:
                    st.session_state.data['询盘时间'] = pd.to_datetime(st.session_state.data['询盘时间'], errors='coerce')
            except Exception:
                pass
    except Exception as e:
        # 静默失败，不在界面上显示错误
        pass


def group_data_by_month(df: pd.DataFrame):
    """按月分组数据"""
    monthly = {}
    if df is None or df.empty or '询盘时间' not in df.columns:
        return monthly
    for _, row in df.iterrows():
        time_value = row.get('询盘时间', '')
        if pd.notna(time_value) and time_value != '':
            try:
                date_obj = pd.to_datetime(time_value, errors='coerce') if isinstance(time_value, str) else time_value
                if pd.notna(date_obj):
                    key = date_obj.strftime('%Y年%m月')
                    if key not in monthly:
                        monthly[key] = []
                    monthly[key].append(row)
            except Exception:
                monthly.setdefault('未知', []).append(row)
    return monthly


def filter_by_time(df: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """按时间范围过滤数据"""
    if df is None or df.empty or '询盘时间' not in df.columns:
        return df
    try:
        s = pd.to_datetime(start_date)
        e = pd.to_datetime(end_date)
        mask = (df['询盘时间'] >= s) & (df['询盘时间'] <= e)
        return df.loc[mask]
    except Exception:
        return df


# ========== 页面搭建 ==========
# 确保在正确的 Streamlit 上下文中
try:
    st.set_page_config(page_title="阿里国际业务智能复盘工具 - 在线版", layout="wide")
except Exception:
    # 如果页面已配置，忽略错误
    pass

st.title("阿里国际业务智能复盘工具 - 在线版")
st.caption("© 版权所有 - jonjiang | 云端部署版")

# 初始化
ensure_output_dir()

# 检查导入错误
if AliBusinessAnalyzer is None:
    show_import_error()

init_state()

# 首次加载时自动加载保存的数据（静默）
if "data_loaded" not in st.session_state:
    load_saved_data_silently()
    st.session_state.data_loaded = True


# ====== Sidebar：全局操作 ======
with st.sidebar:
    st.header("全局操作")

    # 导入 Excel
    uploaded_files = st.file_uploader("导入Excel（可多选 .xlsx/.xls）", type=["xlsx", "xls"], accept_multiple_files=True)
    if uploaded_files:
        try:
            original = st.session_state.analyzer.data.copy() if st.session_state.analyzer.data is not None else None
            for uf in uploaded_files:
                bytes_data = uf.read()
                # 将上传内容保存为临时文件，再交给 analyzer 读取
                upload_dir = os.path.join("output", "uploads")
                os.makedirs(upload_dir, exist_ok=True)
                safe_name = uf.name if uf.name else f"upload_{int(time.time()*1000)}.xlsx"
                temp_path = os.path.join(upload_dir, safe_name)
                with open(temp_path, 'wb') as tmpf:
                    tmpf.write(bytes_data)
                # 使用现有读取逻辑（需要文件路径）
                st.session_state.analyzer.read_excel(temp_path)
                # 合并数据
                if original is not None and not original.empty:
                    combined = pd.concat([original, st.session_state.analyzer.data], ignore_index=True)
                else:
                    combined = st.session_state.analyzer.data

                # 去重（客户名称、询盘时间、询价产品）
                dedup_cols = [c for c in ['客户名称', '询盘时间', '询价产品'] if c in combined.columns]
                if dedup_cols:
                    combined = combined.drop_duplicates(subset=dedup_cols, keep='last')
                original = combined

            st.session_state.analyzer.data = original
            st.session_state.data = original
            # 统一将'询盘时间'转换为datetime，确保后续筛选完整准确
            try:
                if st.session_state.data is not None and '询盘时间' in st.session_state.data.columns:
                    st.session_state.data['询盘时间'] = pd.to_datetime(st.session_state.data['询盘时间'], errors='coerce')
            except Exception:
                pass
            st.success(f"成功导入，当前共有 {len(original) if original is not None else 0} 条记录")
        except Exception as e:
            st.error(f"导入失败：{e}")

    # 历史数据手动加载
    if st.button("加载历史保存数据", use_container_width=True):
        try:
            load_saved_data_silently()
            st.session_state.data = st.session_state.analyzer.data
            if st.session_state.data is not None:
                st.success(f"已加载 {len(st.session_state.data)} 条历史数据")
            else:
                st.info("未找到保存的历史数据")
        except Exception as e:
            st.error(f"加载失败：{e}")

    st.markdown("---")

    # 时间范围
    st.subheader("时间范围")
    # 默认显示全部时间，避免仅显示最近月份
    time_range = st.selectbox("选择时间段", ["最近7天", "最近30天", "最近90天", "全部时间", "自定义"], index=3)
    today = datetime.now()
    if time_range == "最近7天":
        start_date_default, end_date_default = today - timedelta(days=7), today
    elif time_range == "最近30天":
        start_date_default, end_date_default = today - timedelta(days=30), today
    elif time_range == "最近90天":
        start_date_default, end_date_default = today - timedelta(days=90), today
    else:
        start_date_default, end_date_default = today - timedelta(days=30), today

    if time_range == "全部时间" and st.session_state.data is not None and '询盘时间' in st.session_state.data.columns:
        try:
            start_date_default = pd.to_datetime(st.session_state.data['询盘时间'].min())
            end_date_default = pd.to_datetime(st.session_state.data['询盘时间'].max())
        except Exception:
            pass

    # 无论是否自定义，都提供日期微调，确保有显式日期筛选
    start_date = st.date_input("开始日期", value=start_date_default.date())
    end_date = st.date_input("结束日期", value=end_date_default.date())
    start_dt = datetime.combine(start_date, datetime.min.time())
    end_dt = datetime.combine(end_date, datetime.max.time())

    st.markdown("---")

    # 保存/导出区
    if st.session_state.data is not None and not st.session_state.data.empty:
        if st.button("保存所有数据为 saved_data.xlsx", use_container_width=True):
            try:
                st.session_state.analyzer.data = st.session_state.data
                st.session_state.analyzer.export_data("saved_data.xlsx", 'excel', group_by_month=True)
                st.success("已保存到 saved_data.xlsx")
            except Exception as e:
                st.error(f"保存失败：{e}")


# ====== Tabs：功能区 ======
tab1, tab2, tab3, tab4 = st.tabs(["数据预览", "图表展示", "生成报告", "智能提醒"]) 


with tab1:
    st.subheader("数据预览与筛选")
    df = st.session_state.data
    if df is None or df.empty:
        st.info("请在左侧导入Excel或加载历史数据。")
    else:
        # 时间过滤
        filtered = filter_by_time(df, start_dt, end_dt)
        st.session_state.filtered_data = filtered

        # 筛选条件
        st.markdown("##### 筛选条件")
        filter_columns = ['咨询方式', '跟进等级', '客户层级', '所属大洲', '国家', '跟进人']
        cols = st.columns(len(filter_columns))
        active_filters = {}
        for i, col_name in enumerate(filter_columns):
            if col_name in filtered.columns:
                unique_values = ["全部"] + sorted([str(x) for x in filtered[col_name].dropna().unique().tolist()])
                selected = cols[i].selectbox(col_name, options=unique_values, index=0)
                if selected and selected != "全部":
                    active_filters[col_name] = selected

        # 应用筛选
        for k, v in active_filters.items():
            if k in filtered.columns:
                filtered = filtered[filtered[k].astype(str).str.contains(str(v), na=False)]

        st.markdown("---")

        # 可编辑表格
        st.markdown("##### 数据表（可编辑）")
        edited_df = st.data_editor(filtered.reset_index(drop=True), use_container_width=True, num_rows="dynamic")

        # 同步变更按钮
        if st.button("同步变更到全部数据（根据当前筛选前的行序）"):
            try:
                # 将编辑后的数据写回到原始 DataFrame
                # 简化策略：用时间过滤后的索引匹配更新（若列匹配不上将跳过）
                base = filter_by_time(st.session_state.data, start_dt, end_dt)
                if len(base) >= len(edited_df):
                    # 按位置回写
                    idxs = base.index.tolist()[:len(edited_df)]
                    for j, ridx in enumerate(idxs):
                        for col in st.session_state.analyzer.standard_columns:
                            if col in edited_df.columns and col in st.session_state.data.columns:
                                st.session_state.data.at[ridx, col] = edited_df.at[j, col]
                    st.success("已同步变更到原始数据")
                else:
                    st.warning("当前数据对齐复杂，未自动覆盖全部，请导出编辑后再导入以确保一致性。")
            except Exception as e:
                st.error(f"同步失败：{e}")

        # 删除选中行提示
        st.info("如需删除，请在表格编辑区删除行后点击同步，或导出后在Excel中处理再导入。")

        # 月度分组
        st.markdown("---")
        st.markdown("##### 月度数据预览")
        monthly = group_data_by_month(filtered)
        month_keys = list(monthly.keys())
        if month_keys:
            sel_month = st.selectbox("选择月份", month_keys, index=0)
            month_df = pd.DataFrame(monthly[sel_month]) if isinstance(monthly[sel_month], list) else monthly[sel_month]
            st.dataframe(month_df, use_container_width=True)
        else:
            st.caption("无可显示的月份分组。")

        # 导出
        st.markdown("---")
        st.markdown("##### 导出")
        export_format = st.selectbox("导出格式", ["Excel (.xlsx)", "CSV (.csv)"])
        if st.button("导出当前筛选结果"):
            try:
                temp_file = "output/export_online_temp.xlsx" if export_format.startswith("Excel") else "output/export_online_temp.csv"
                st.session_state.analyzer.data = filtered
                st.session_state.analyzer.export_data(temp_file, 'excel' if export_format.startswith("Excel") else 'csv', group_by_month=False)
                with open(temp_file, 'rb') as f:
                    btn = st.download_button(
                        label="点击下载导出文件",
                        data=f.read(),
                        file_name=os.path.basename(temp_file),
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' if export_format.startswith("Excel") else 'text/csv'
                    )
                st.success("导出完成")
            except Exception as e:
                st.error(f"导出失败：{e}")


with tab2:
    st.subheader("图表展示")
    df = st.session_state.data
    if df is None or df.empty:
        st.info("请先导入数据或加载历史数据。")
    else:
        filtered = filter_by_time(df, start_dt, end_dt)
        if filtered is None or filtered.empty:
            st.warning("所选时间段内没有数据")
        else:
            try:
                # 临时替换 analyzer 数据并生成图表（与桌面版一致）
                original = st.session_state.analyzer.data
                st.session_state.analyzer.data = filtered
                st.session_state.analyzer.generate_visualizations()
                st.session_state.analyzer.data = original

                st.success(f"图表生成完成（{len(filtered)} 条记录）")

                chart_files = {
                    '地区分布图': './output/continent_distribution.png',
                    '国家分布图': './output/country_distribution.png',
                    '产品热度图': './output/product_popularity.png',
                    '时间趋势图': './output/daily_trend.png'
                }

                cols = st.columns(2)
                i = 0
                for title, path in chart_files.items():
                    if os.path.exists(path) and Image is not None:
                        with cols[i % 2]:
                            st.markdown(f"###### {title}")
                            st.image(Image.open(path), use_column_width=True)
                    else:
                        with cols[i % 2]:
                            st.info(f"{title} 暂无可用图像")
                    i += 1
            except Exception as e:
                st.error(f"生成图表失败：{e}")

        # 生成可视化大屏（如可用）
        st.markdown("---")
        if DASHBOARD_AVAILABLE and st.button("生成并下载可视化大屏 HTML"):
            try:
                original = st.session_state.analyzer.data
                st.session_state.analyzer.data = filtered
                st.session_state.analyzer.export_data("saved_data.xlsx", 'excel', group_by_month=False)
                dashboard = BusinessDashboard(data_file="saved_data.xlsx")
                dashboard.create_dashboard()
                html_path = os.path.abspath('./output/business_dashboard.html')
                if os.path.exists(html_path):
                    with open(html_path, 'rb') as f:
                        st.download_button("下载大屏HTML", f, file_name="business_dashboard.html", mime="text/html")
                    st.success("大屏已生成，可下载HTML离线查看")
                else:
                    st.warning("未找到生成的大屏HTML文件")
            except Exception as e:
                st.error(f"生成大屏失败：{e}")
            finally:
                st.session_state.analyzer.data = original


with tab3:
    st.subheader("生成报告（AI智能分析版）")
    df = st.session_state.data
    if df is None or df.empty:
        st.info("请先导入数据或加载历史数据。")
    else:
        filtered = filter_by_time(df, start_dt, end_dt)
        if filtered is None or filtered.empty:
            st.warning("所选时间段内没有数据")
        else:
            if st.button("生成报告"):
                try:
                    original = st.session_state.analyzer.data
                    st.session_state.analyzer.data = filtered
                    report_file = st.session_state.analyzer.generate_report(
                        user_date_range=(start_dt.strftime('%Y-%m-%d'), end_dt.strftime('%Y-%m-%d'))
                    )
                    st.session_state.analyzer.data = original

                    if report_file and os.path.exists(report_file):
                        with open(report_file, 'rb') as f:
                            st.download_button("下载报告", f, file_name=os.path.basename(report_file), mime="text/plain")
                        st.success("报告生成完成")
                    else:
                        st.warning("未找到报告文件")
                except Exception as e:
                    st.error(f"生成报告失败：{e}")


with tab4:
    st.subheader("智能提醒 - 6大核心预警")
    df = st.session_state.data
    if df is None or df.empty:
        st.info("请先导入数据或加载历史数据。")
    else:
        filtered = filter_by_time(df, start_dt, end_dt)
        if filtered is None or filtered.empty:
            st.warning("所选时间段内没有数据")
        else:
            try:
                original = st.session_state.analyzer.data
                st.session_state.analyzer.data = filtered
                alerts = st.session_state.analyzer.get_smart_alerts()
                st.session_state.analyzer.data = original

                if not alerts:
                    st.success("当前无需要关注的提醒，客户跟进状态良好。")
                else:
                    # 分类汇总
                    categories = {}
                    for alert in alerts:
                        cat = alert.get('category', '其他')
                        categories[cat] = categories.get(cat, 0) + 1

                    st.markdown("###### 提醒分类汇总")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        for cat, count in categories.items():
                            st.write(f"- {cat}：{count} 条")

                    st.markdown("---")

                    # 详细列表
                    for i, alert in enumerate(alerts, 1):
                        priority = alert.get('priority', 'medium')
                        icon = '🔴' if priority == 'high' else ('🟡' if priority == 'medium' else '🟢')
                        with st.expander(f"{icon} {i}. {alert.get('message', '提醒')}"):
                            st.write(f"分类：{alert.get('category', '其他')}")
                            st.write(f"优先级：{priority}")
                            if 'suggestion' in alert:
                                st.write(f"建议：{alert['suggestion']}")

                    # 导出提醒
                    if st.button("导出提醒为文本"):
                        try:
                            txt_path = f"output/智能提醒_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                            with open(txt_path, 'w', encoding='utf-8') as f:
                                f.write("=" * 80 + "\n")
                                f.write("阿里国际业务智能提醒报告\n")
                                f.write("Ali International Business Smart Alerts Report\n")
                                f.write("=" * 80 + "\n\n")
                                f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                                f.write(f"提醒总数: {len(alerts)} 条\n\n")
                                # 分类
                                f.write("【分类汇总】\n")
                                for cat, count in categories.items():
                                    f.write(f"  {cat}: {count} 条\n")
                                f.write("\n")
                                # 详情
                                current_category = None
                                for i, a in enumerate(alerts, 1):
                                    cat = a.get('category', '其他')
                                    if cat != current_category:
                                        f.write("\n" + "=" * 80 + "\n")
                                        f.write(f"{cat}\n")
                                        f.write("=" * 80 + "\n")
                                        current_category = cat
                                    f.write(f"\n{i}. {a.get('message','')}\n")
                                    if 'suggestion' in a:
                                        f.write(f"   建议: {a['suggestion']}\n")
                                    f.write(f"   优先级: {a.get('priority','medium').upper()}\n")

                            with open(txt_path, 'rb') as f:
                                st.download_button("下载提醒文本", f, file_name=os.path.basename(txt_path), mime="text/plain")
                            st.success("提醒已导出")
                        except Exception as e:
                            st.error(f"导出失败：{e}")
            except Exception as e:
                st.error(f"获取提醒失败：{e}")


# ===== 页脚 =====
st.markdown("---")
st.caption("部署提示：可直接使用 streamlit 在云主机/平台运行；若在无持久磁盘的环境运行，请注意导出的文件需立即下载保存。")
