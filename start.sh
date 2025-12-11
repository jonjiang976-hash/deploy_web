#!/bin/bash
# 阿里国际业务智能复盘工具 - 启动脚本（Linux/Mac）

echo "=========================================="
echo "  阿里国际业务智能复盘工具 - 网页版"
echo "=========================================="
echo ""

# 检查Python版本
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python版本: $python_version"

# 检查Streamlit是否安装
if ! command -v streamlit &> /dev/null; then
    echo "错误: Streamlit 未安装"
    echo "请运行: pip install -r requirements_web.txt"
    exit 1
fi

# 创建必要的目录
mkdir -p output/uploads

# 启动应用
echo ""
echo "正在启动应用..."
echo "访问地址: http://localhost:8501"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

streamlit run ali_online.py --server.port 8501 --server.address 0.0.0.0

