# Streamlit Cloud 快速修复指南

## ❌ 当前错误

```
无法导入 AliBusinessAnalyzer: No module named 'matplotlib'
```

## ✅ 解决方案

### 方法1：添加 requirements.txt 文件（推荐）

**问题原因**: Streamlit Cloud 只读取 `requirements.txt` 文件，不会读取 `requirements_web.txt`

**解决步骤**:

1. **在您的 GitHub 仓库根目录添加 `requirements.txt` 文件**

   文件内容：
   ```txt
   streamlit>=1.28.0
   pandas>=2.0.0
   openpyxl>=3.1.0
   xlrd>=2.0.1
   Pillow>=10.0.0
   matplotlib>=3.7.0
   plotly>=5.14.0
   reportlab>=4.0.0
   python-docx>=1.0.0
   folium>=0.14.0
   ```

2. **提交并推送**
   ```bash
   git add requirements.txt
   git commit -m "Add requirements.txt for Streamlit Cloud"
   git push
   ```

3. **在 Streamlit Cloud 重新部署**
   - 进入您的应用设置
   - 点击 "Reboot app" 或等待自动重新部署

### 方法2：使用部署包中的文件

本部署包已包含 `requirements.txt` 文件，您只需要：

1. **将 `requirements.txt` 复制到仓库根目录**
2. **提交并推送**
3. **重新部署**

## 📋 文件检查清单

确保您的 GitHub 仓库包含：

- [x] `requirements.txt` - **必需！** Streamlit Cloud 会自动读取
- [x] `ali_online.py` - 主程序
- [x] `ali_business_analyzer.py` - 核心分析器
- [x] `ali_business_dashboard.py` - 大屏功能（可选）

## 🔍 验证步骤

1. **检查文件是否存在**
   - 在 GitHub 仓库页面，确认 `requirements.txt` 在根目录
   - 点击文件查看内容是否正确

2. **检查依赖是否完整**
   - 确保 `matplotlib` 在 `requirements.txt` 中
   - 确保所有必需的包都已列出

3. **重新部署**
   - Streamlit Cloud 会自动检测更改
   - 或手动点击 "Reboot app"

## 📝 完整的 requirements.txt 内容

```txt
# 阿里国际业务智能复盘工具 - Streamlit Cloud 部署依赖
# Streamlit Cloud 会自动读取此文件安装依赖

# Web框架（必需）
streamlit>=1.28.0

# 数据处理（必需）
pandas>=2.0.0
openpyxl>=3.1.0
xlrd>=2.0.1

# 图像处理（必需）
Pillow>=10.0.0

# 数据可视化（必需）
matplotlib>=3.7.0
plotly>=5.14.0

# PDF和文档生成（必需）
reportlab>=4.0.0

# Word文档支持（可选）
python-docx>=1.0.0

# 地图可视化（可选）
folium>=0.14.0
```

## ⚠️ 重要提示

1. **文件名必须是 `requirements.txt`**
   - ❌ 不要使用 `requirements_web.txt`
   - ✅ 必须使用 `requirements.txt`

2. **文件必须在仓库根目录**
   - 不是在子目录中
   - 不是在 `.streamlit/` 目录中

3. **重新部署后等待**
   - 构建通常需要 2-5 分钟
   - 查看构建日志了解进度

## 🎯 快速操作

如果您使用本部署包：

1. 复制 `deploy_web/requirements.txt` 到您的 GitHub 仓库根目录
2. 提交并推送
3. Streamlit Cloud 会自动重新部署

---

**修复后，应用应该可以正常运行！** 🎉

