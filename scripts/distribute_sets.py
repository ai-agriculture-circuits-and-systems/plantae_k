#!/usr/bin/env python3
"""
将主类别目录下的 sets 文件分配到各个子类别目录
根据文件名前缀（如 apple_d001 -> diseased, apple_h001 -> healthy）进行分配
"""

import os
import shutil
from pathlib import Path
from collections import defaultdict

def get_subcategory_from_filename(filename, main_category):
    """
    根据文件名确定子类别
    例如: apple_d001 -> diseased, apple_h001 -> healthy
    """
    # 移除主类别前缀
    name = filename.replace(f"{main_category}_", "")
    
    # 检查是否有子类别标识符
    if name.startswith('d'):
        return 'diseased'
    elif name.startswith('h'):
        return 'healthy'
    else:
        # 尝试其他可能的模式
        # 如果无法确定，返回 None
        return None

def distribute_sets(main_cat_dir: Path, main_category: str):
    """将主类别目录下的 sets 文件分配到子类别目录"""
    sets_dir = main_cat_dir / 'sets'
    
    if not sets_dir.exists():
        print(f"  {main_category}: 没有 sets 目录，跳过")
        return
    
    print(f"\n处理 {main_category}...")
    
    # 获取所有子类别目录
    subcategories = {}
    for item in main_cat_dir.iterdir():
        if item.is_dir() and item.name not in ['sets', 'labelmap.json']:
            subcategories[item.name] = item
    
    if not subcategories:
        print(f"  警告: {main_category} 没有子类别目录")
        return
    
    print(f"  找到子类别: {list(subcategories.keys())}")
    
    # 读取所有 sets 文件
    set_files = ['train.txt', 'val.txt', 'test.txt', 'all.txt', 'train_val.txt']
    
    for set_file in set_files:
        source_file = sets_dir / set_file
        if not source_file.exists():
            continue
        
        print(f"  处理 {set_file}...")
        
        # 读取文件内容
        with open(source_file, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        
        # 按子类别分组
        subcat_items = defaultdict(list)
        unknown_items = []
        
        for line in lines:
            subcat = get_subcategory_from_filename(line, main_category)
            if subcat and subcat in subcategories:
                subcat_items[subcat].append(line)
            else:
                unknown_items.append(line)
        
        # 为每个子类别创建 sets 目录并写入文件
        for subcat_name, items in subcat_items.items():
            subcat_dir = subcategories[subcat_name]
            subcat_sets_dir = subcat_dir / 'sets'
            subcat_sets_dir.mkdir(parents=True, exist_ok=True)
            
            target_file = subcat_sets_dir / set_file
            with open(target_file, 'w', encoding='utf-8') as f:
                for item in sorted(items):
                    f.write(f"{item}\n")
            
            print(f"    {subcat_name}: {len(items)} 个条目")
        
        if unknown_items:
            print(f"    警告: {len(unknown_items)} 个条目无法分类: {unknown_items[:5]}")
    
    # 删除主类别目录下的 sets 目录
    print(f"  删除 {sets_dir}")
    shutil.rmtree(sets_dir)

def main():
    """主函数"""
    dataset_root = Path('/home/yuhanlin/Database/local/plantae_k')
    
    print("="*60)
    print("分配 sets 文件到子类别目录")
    print("="*60)
    
    # 获取所有主类别目录
    main_categories = []
    for item in dataset_root.iterdir():
        if item.is_dir() and item.name not in ['annotations', 'data', 'scripts']:
            # 检查是否有 sets 目录
            if (item / 'sets').exists():
                main_categories.append((item.name, item))
    
    print(f"\n找到 {len(main_categories)} 个需要处理的主类别:")
    for name, _ in main_categories:
        print(f"  - {name}")
    
    # 处理每个主类别
    for main_category, main_cat_dir in main_categories:
        distribute_sets(main_cat_dir, main_category)
    
    print("\n" + "="*60)
    print("完成！")
    print("="*60)

if __name__ == '__main__':
    main()

