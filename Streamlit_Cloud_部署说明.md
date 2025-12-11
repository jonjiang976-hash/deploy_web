# Streamlit Cloud 部署说明

## 🚀 快速部署步骤

### 1. 准备代码仓库

确保您的代码已推送到 GitHub 仓库，包含以下文件：

**必需文件：**
- ✅ `ali_online.py` - 主程序
- ✅ `ali_business_analyzer.py` - 核心分析器
- ✅ `ali_business_dashboard.py` - 大屏功能（可选）
- ✅ `requirements.txt` - **重要！** Streamlit Cloud 会自动读取此文件

**可选文件：**
- `config.json` - 配置文件
- `.streamlit/config.toml` - Streamlit 配置

### 2. 部署到 Streamlit Cloud

1. **访问 Streamlit Cloud**
   - 打开 https://streamlit.io/cloud
   - 使用 GitHub 账号登录

2. **创建新应用**
   - 点击 "New app"
   - 选择您的 GitHub 仓库
   - 选择分支（通常是 `main` 或 `master`）

3. **配置应用**
   - **Main file path**: `ali_online.py`
   - **Python version**: 3.11（推荐）或 3.10
   - Streamlit Cloud 会自动读取 `requirements.txt` 安装依赖

4. **部署**
   - 点击 "Deploy!"
   - 等待构建完成（通常 2-5 分钟）

### 3. 访问应用

部署完成后，您会获得一个 URL，例如：
```
https://your-app-name.streamlit.app
```

## ⚠️ 重要注意事项

### requirements.txt 文件

**Streamlit Cloud 只读取 `requirements.txt` 文件！**

确保您的仓库根目录有 `requirements.txt` 文件，包含所有依赖：

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

### 文件结构

推荐的文件结构：
```
your-repo/
├── ali_online.py              # 主程序
├── ali_business_analyzer.py   # 核心分析器
├── ali_business_dashboard.py  # 大屏功能
├── requirements.txt           # 依赖文件（必需！）
├── config.json                # 配置文件（可选）
└── .streamlit/
    └── config.toml            # Streamlit配置（可选）
```

### 常见问题

#### 问题1: 找不到模块（如 matplotlib）

**原因**: `requirements.txt` 文件缺失或依赖未包含

**解决**:
1. 确保 `requirements.txt` 在仓库根目录
2. 确保所有依赖都列在 `requirements.txt` 中
3. 重新部署应用

#### 问题2: 导入错误

**原因**: 某些模块在 Streamlit Cloud 环境中不可用（如 tkinter）

**解决**: 
- 代码已修复，tkinter 现在是可选依赖
- 如果仍有问题，检查代码中的导入语句

#### 问题3: 构建失败

**解决**:
1. 检查 `requirements.txt` 格式是否正确
2. 确保 Python 版本兼容（推荐 3.10 或 3.11）
3. 查看构建日志中的错误信息

## 📝 部署检查清单

部署前确认：
- [ ] `requirements.txt` 文件存在且包含所有依赖
- [ ] `ali_online.py` 文件存在
- [ ] `ali_business_analyzer.py` 文件存在
- [ ] 所有文件已推送到 GitHub
- [ ] 代码中没有硬编码的本地路径

## 🔄 更新应用

1. 修改代码后，推送到 GitHub
2. Streamlit Cloud 会自动检测更改并重新部署
3. 或手动点击 "Reboot app" 重新部署

## 📞 需要帮助？

- 查看 Streamlit Cloud 文档: https://docs.streamlit.io/streamlit-community-cloud
- 查看应用日志: 在 Streamlit Cloud 控制台查看 "Logs"
- 检查构建日志: 查看 "Build logs" 了解构建过程

---

**提示**: 如果遇到依赖问题，确保 `requirements.txt` 文件在仓库根目录，并且所有必需的包都已列出。

