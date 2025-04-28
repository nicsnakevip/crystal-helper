# Crystal Helper

水晶信息查询助手，帮助快速查询水晶的分类信息。

## 项目结构

```
crystal-helper/
├── src/                # 源代码目录
│   └── userscript/    # 浏览器脚本
├── data/              # 数据文件目录
│   ├── raw/          # 原始数据
│   └── processed/    # 处理后的数据
├── scripts/          # 数据处理脚本
└── docs/             # 文档
```

## 功能说明

1. 数据处理
   - 从Excel文件读取水晶数据
   - 处理并转换为JSON格式
   - 自动更新到GitHub仓库

2. 浏览器插件
   - 实时搜索水晶信息
   - 显示完整分类路径
   - 支持模糊匹配

## 使用说明

1. 更新数据
   ```bash
   cd scripts
   python process_crystal_data.py
   ```

2. 安装浏览器脚本
   - 安装Tampermonkey插件
   - 导入`src/userscript/crystal_helper.user.js`

## 数据格式

1. 输入数据（Excel）
   - A列：分类路径
   - B列：具体类目
   - C列：搜索关键词

2. 输出数据（JSON）
   ```json
   {
     "name": "分类路径",
     "category": "具体类目",
     "searchKey": "搜索关键词"
   }
   ```

## 维护说明

1. 更新数据流程
   - 修改`data/raw/水晶.xlsx`
   - 运行数据处理脚本
   - 提交更新到GitHub

2. 修改脚本流程
   - 更新脚本代码
   - 修改版本号
   - 提交更新到GitHub 