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

# 更新crystal-helper仓库
echo "更新crystal-helper仓库..."
git add -A
git commit -m "自动更新数据 - $(date '+%Y-%m-%d %H:%M:%S')"
git push

# 同步到crystal_data仓库
echo "同步到crystal_data仓库..."
CRYSTAL_DATA_DIR="/Users/wei/maiterial/kaifa/crystal_data"

# 如果crystal_data目录不存在，则克隆
if [ ! -d "$CRYSTAL_DATA_DIR" ]; then
    echo "克隆crystal_data仓库..."
    cd /Users/wei/maiterial/kaifa
    git clone https://github.com/nicsnakevip/crystal_data.git
fi

# 复制文件到crystal_data仓库
echo "复制文件..."
cp "$SCRIPT_DIR/data/processed/crystal_data.json" "$CRYSTAL_DATA_DIR/"
cp "$SCRIPT_DIR/src/userscript/crystal_helper.user.js" "$CRYSTAL_DATA_DIR/"

# 提交并推送更改
cd "$CRYSTAL_DATA_DIR"
git add crystal_data.json crystal_helper.user.js
git commit -m "自动更新数据 - $(date '+%Y-%m-%d %H:%M:%S')"
git push

echo "更新完成！"

# 等待用户按回车键后退出
echo -e "\n按回车键退出..."
read 