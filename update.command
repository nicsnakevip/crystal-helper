#!/bin/bash

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# 切换到项目目录
cd "$SCRIPT_DIR"

# 设置Python环境（如果需要的话）
# source /path/to/your/venv/bin/activate  # 如果您使用虚拟环境，取消这行注释

# 检查并安装所需的Python包
echo "检查并安装所需的Python包..."
pip install pandas openpyxl gitpython --quiet

# 运行Python脚本
echo "开始处理数据..."
python scripts/process_crystal_data.py

# 强制更新Git仓库
echo "更新Git仓库..."
git add -A
git commit -m "自动更新数据 - $(date '+%Y-%m-%d %H:%M:%S')"
git push

echo "更新完成！"

# 等待用户按回车键后退出
echo -e "\n按回车键退出..."
read 