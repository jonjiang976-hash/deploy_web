@echo off
chcp 65001 >nul
cls
echo ==========================================
echo   阿里国际业务智能复盘工具 - 网页版
echo ==========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: Python 未安装或未添加到PATH
    pause
    exit /b 1
)

REM 检查Streamlit是否安装
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo 错误: Streamlit 未安装
    echo 请运行: pip install -r requirements_web.txt
    pause
    exit /b 1
)

REM 创建必要的目录
if not exist "output\uploads" mkdir "output\uploads"

REM 启动应用
echo.
echo 正在启动应用...
echo 访问地址: http://localhost:8501
echo.
echo 按 Ctrl+C 停止服务
echo.

streamlit run ali_online.py --server.port 8501 --server.address 0.0.0.0

pause

