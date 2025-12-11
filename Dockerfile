# 阿里国际业务智能复盘工具 - Docker部署文件
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# 复制依赖文件
COPY requirements_web.txt .

# 安装依赖
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements_web.txt

# 复制应用文件
COPY ali_online.py .
COPY ali_business_analyzer.py .
COPY ali_business_dashboard.py .
COPY .streamlit ./.streamlit

# 创建输出目录
RUN mkdir -p output/uploads

# 暴露端口
EXPOSE 8501

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8501/_stcore/health')" || exit 1

# 启动命令
CMD ["streamlit", "run", "ali_online.py", "--server.port=8501", "--server.address=0.0.0.0"]

