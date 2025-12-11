# 阿里国际业务智能复盘工具 - 网页版部署包

## 📦 文件说明

```
deploy_web/
├── ali_online.py              # 主程序文件（Streamlit应用）
├── ali_business_analyzer.py   # 核心分析器
├── ali_business_dashboard.py  # 可视化大屏功能
├── config.json                # 配置文件（可选）
├── requirements_web.txt       # 依赖包列表
├── start.sh                   # Linux/Mac 启动脚本
├── start.bat                  # Windows 启动脚本
├── .streamlit/
│   └── config.toml           # Streamlit配置文件
├── output/                    # 输出目录
│   └── uploads/              # 上传文件目录
└── README.md                  # 本文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements_web.txt
```

### 2. 启动应用

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

**或直接使用命令:**
```bash
streamlit run ali_online.py --server.port 8501 --server.address 0.0.0.0
```

### 3. 访问应用

打开浏览器访问: **http://localhost:8501**

## 🌐 服务器部署

### 方式一：直接部署（推荐）

1. **上传文件到服务器**
   ```bash
   # 将整个 deploy_web 目录上传到服务器
   scp -r deploy_web user@your-server:/path/to/app/
   ```

2. **SSH连接到服务器**
   ```bash
   ssh user@your-server
   cd /path/to/app/deploy_web
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements_web.txt
   ```

4. **启动应用**
   ```bash
   # 使用nohup在后台运行
   nohup streamlit run ali_online.py --server.port 8501 --server.address 0.0.0.0 > app.log 2>&1 &
   
   # 或使用screen
   screen -S ali_app
   streamlit run ali_online.py --server.port 8501 --server.address 0.0.0.0
   # 按 Ctrl+A 然后 D 退出screen
   ```

5. **配置Nginx反向代理（可选）**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8501;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "upgrade";
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

### 方式二：使用Docker部署

1. **创建Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements_web.txt .
   RUN pip install --no-cache-dir -r requirements_web.txt
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["streamlit", "run", "ali_online.py", "--server.port=8501", "--server.address=0.0.0.0"]
   ```

2. **构建和运行**
   ```bash
   docker build -t ali-business-web .
   docker run -d -p 8501:8501 --name ali-app ali-business-web
   ```

### 方式三：使用Streamlit Cloud（最简单）

**重要：Streamlit Cloud 需要 `requirements.txt` 文件！**

1. **确保 `requirements.txt` 文件在仓库根目录**
   - 本部署包已包含 `requirements.txt`
   - Streamlit Cloud 会自动读取此文件安装依赖

2. **将代码推送到GitHub**
   ```bash
   git add .
   git commit -m "Deploy to Streamlit Cloud"
   git push
   ```

3. **部署到Streamlit Cloud**
   - 访问 https://streamlit.io/cloud
   - 使用GitHub账号登录
   - 点击 "New app"
   - 选择您的仓库和分支
   - **Main file path**: `ali_online.py`
   - 点击 "Deploy!"

4. **等待部署完成**
   - 通常需要 2-5 分钟
   - 查看构建日志了解进度

5. **访问应用**
   - 部署完成后会获得一个 URL
   - 例如：`https://your-app-name.streamlit.app`

**详细说明请查看 `Streamlit_Cloud_部署说明.md`**

## ⚙️ 配置说明

### 修改端口

编辑 `.streamlit/config.toml`:
```toml
[server]
port = 8501  # 修改为您想要的端口
```

### 修改配置

编辑 `config.json`（如果存在）或使用应用内的配置功能。

## 📋 系统要求

- Python 3.8 或更高版本
- 至少 2GB 可用内存
- 网络连接（用于下载依赖）

## 🔧 故障排查

### 问题1: 端口被占用

**解决方案:**
```bash
# 查找占用端口的进程
lsof -i :8501  # Linux/Mac
netstat -ano | findstr :8501  # Windows

# 修改端口
# 编辑 .streamlit/config.toml 或使用 --server.port 参数
streamlit run ali_online.py --server.port 8502
```

### 问题2: 依赖安装失败

**解决方案:**
```bash
# 升级pip
pip install --upgrade pip

# 单独安装问题包
pip install streamlit pandas matplotlib pillow openpyxl plotly reportlab
```

### 问题3: 无法访问应用

**检查清单:**
- [ ] 防火墙是否允许8501端口
- [ ] 服务器地址是否正确（0.0.0.0 允许外部访问）
- [ ] 应用是否正在运行
- [ ] 查看日志文件 app.log

## 📝 功能说明

- ✅ Excel数据导入
- ✅ 数据预览和筛选
- ✅ 智能数据分析
- ✅ 图表生成
- ✅ 报告生成（TXT/PDF）
- ✅ 智能提醒
- ✅ 数据导出
- ✅ 可视化大屏

## 🔒 安全建议

1. **生产环境建议:**
   - 使用HTTPS（配置SSL证书）
   - 设置访问密码（Streamlit支持）
   - 限制IP访问（通过防火墙或Nginx）
   - 定期备份数据

2. **设置密码:**
   ```bash
   # 创建 .streamlit/secrets.toml
   [password]
   password = "your-secure-password"
   ```

## 📞 技术支持

如有问题，请查看：
- 部署说明文档
- 应用日志文件
- GitHub Issues（如果有）

---

© 版权所有 - jonjiang | 2024-12-11

