import subprocess
import sys
import logging
from pathlib import Path
from datetime import datetime

# 设置项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# 配置日志
log_dir = PROJECT_ROOT / 'logs'
log_dir.mkdir(exist_ok=True)
log_file = log_dir / 'auto_update.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def run_command(command, cwd=None):
    """运行命令并返回结果"""
    try:
        result = subprocess.run(
            command,
            cwd=cwd or PROJECT_ROOT,
            shell=True,
            text=True,
            capture_output=True
        )
        if result.returncode != 0:
            logging.error(f"命令执行失败: {command}")
            logging.error(f"错误信息: {result.stderr}")
            return False
        logging.info(f"命令执行成功: {command}")
        if result.stdout:
            logging.info(f"输出信息: {result.stdout}")
        return True
    except Exception as e:
        logging.error(f"执行命令时出错: {str(e)}")
        return False

def process_data():
    """处理Excel数据"""
    logging.info("开始处理Excel数据...")
    
    try:
        # 导入process_crystal_data模块
        import process_crystal_data
        process_crystal_data.main()
        logging.info("数据处理完成")
        return True
    except Exception as e:
        logging.error(f"处理数据时出错: {str(e)}")
        return False

def update_git():
    """更新Git仓库"""
    logging.info("开始更新Git仓库...")
    
    # 检查是否有更改
    status = subprocess.run(
        "git status --porcelain",
        cwd=PROJECT_ROOT,
        shell=True,
        text=True,
        capture_output=True
    )
    
    if not status.stdout.strip():
        logging.info("没有检测到文件变更")
        return True
    
    # 获取更改的文件列表
    changed_files = status.stdout.strip().split('\n')
    logging.info(f"检测到以下文件变更:\n{chr(10).join(changed_files)}")
    
    # 提交更改
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commands = [
        "git add .",
        f'git commit -m "自动更新数据 - {timestamp}"',
        "git push"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            logging.error("Git操作失败")
            return False
    
    logging.info("Git仓库更新完成")
    return True

def main():
    """主函数"""
    logging.info("开始执行自动更新...")
    
    # 1. 处理数据
    if not process_data():
        logging.error("数据处理失败，终止更新")
        sys.exit(1)
    
    # 2. 更新Git仓库
    if not update_git():
        logging.error("Git更新失败")
        sys.exit(1)
    
    logging.info("自动更新完成")
    print("✅ 更新成功！数据已经同步到GitHub")

if __name__ == '__main__':
    main() 