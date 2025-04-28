import pandas as pd
import json
import logging
from pathlib import Path
import sys
import os

# 获取项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# 配置日志
log_file = PROJECT_ROOT / 'logs' / 'crystal_process.log'
log_file.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def clean_value(value):
    """清理并转换数据值"""
    if pd.isna(value):  # 处理空值
        return ''
    # 将所有值转换为字符串
    return str(value).strip()

def process_excel_data(excel_file):
    """处理Excel数据"""
    try:
        # 读取Excel文件
        df = pd.read_excel(excel_file, names=['a', 'b', 'c'])
        
        # 清理数据
        df = df.fillna('')
        # 将所有列的数据转换为字符串
        for col in df.columns:
            df[col] = df[col].apply(clean_value)
        
        # 创建结果列表
        result = []
        
        # 处理每一行数据
        for _, row in df.iterrows():
            if row['c']:  # 如果C列有值
                try:
                    # 分割C列的多个关键词
                    keywords = [k.strip() for k in row['c'].split('，') if k.strip()]
                    
                    # 为每个关键词创建一条记录
                    for keyword in keywords:
                        item = {
                            'name': row['a'],  # A列作为分类路径
                            'category': row['b'],  # B列作为类目
                            'searchKey': keyword  # C列的单个关键词
                        }
                        result.append(item)
                except Exception as e:
                    logging.warning(f"处理行数据时出错，跳过此行: {row.to_dict()} - 错误: {str(e)}")
                    continue
        
        return result
        
    except Exception as e:
        logging.error(f"处理Excel数据时出错: {str(e)}")
        raise

def save_json(data, output_file):
    """保存为JSON文件"""
    try:
        # 确保输出目录存在
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存为JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    except Exception as e:
        logging.error(f"保存JSON文件时出错: {str(e)}")
        raise

def main():
    try:
        # 文件路径
        excel_file = PROJECT_ROOT / 'data' / 'raw' / '水晶.xlsx'
        output_file = PROJECT_ROOT / 'data' / 'processed' / 'crystal_data.json'
        
        # 处理数据
        logging.info("开始处理Excel数据...")
        data = process_excel_data(excel_file)
        logging.info(f"数据处理完成，共 {len(data)} 条记录")
        
        # 保存结果
        logging.info("开始保存JSON文件...")
        save_json(data, output_file)
        logging.info(f"文件已保存到: {output_file}")
        
        print(f'处理完成，共生成 {len(data)} 条记录')
        
    except Exception as e:
        logging.error(f"程序执行失败: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 