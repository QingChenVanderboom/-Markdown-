#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试转换器
"""

from md2pdf import convert_markdown_to_html
from pathlib import Path

def main():
    # 测试文件路径
    test_file = Path(__file__).parent / "test_markdown.md"
    output_file = Path(__file__).parent / "test_output.html"
    
    print("测试Markdown转HTML转换器")
    print("=" * 50)
    print(f"输入文件：{test_file}")
    print(f"输出文件：{output_file}")
    
    # 执行转换
    success = convert_markdown_to_html(str(test_file), str(output_file))
    
    if success:
        print("\n转换完成！请检查生成的HTML文件。")
        
        # 读取并显示部分转换结果
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print("\n=== 转换结果预览 ===")
        # 查找body标签内容
        import re
        body_match = re.search(r'<body>(.*?)</body>', content, re.DOTALL)
        if body_match:
            body_content = body_match.group(1)
            # 显示前1000个字符
            preview = body_content[:1000]
            print(preview)
            if len(body_content) > 1000:
                print("\n... (内容已截断)")
    else:
        print("\n转换失败！")

if __name__ == "__main__":
    main()