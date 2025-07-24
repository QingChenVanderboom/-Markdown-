#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown转HTML转换器
自动读取md文件并生成对应的HTML文件
"""

import re
import os
from pathlib import Path

def convert_markdown_to_html(md_file_path, output_html_path=None):
    """
    将Markdown文件转换为HTML文件
    
    Args:
        md_file_path (str): Markdown文件路径
        output_html_path (str): 输出HTML文件路径，如果为None则自动生成
    """
    
    # 读取Markdown文件
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 {md_file_path}")
        return False
    except Exception as e:
        print(f"读取文件时出错：{e}")
        return False
    
    # 如果没有指定输出路径，自动生成
    if output_html_path is None:
        md_path = Path(md_file_path)
        output_html_path = md_path.parent / f"{md_path.stem}.html"
    
    # 转换Markdown为HTML
    html_content = markdown_to_html(md_content)
    
    # 写入HTML文件
    try:
        with open(output_html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"成功生成HTML文件：{output_html_path}")
        return True
    except Exception as e:
        print(f"写入HTML文件时出错：{e}")
        return False

def markdown_to_html(md_content):
    """
    将Markdown内容转换为HTML内容
    
    Args:
        md_content (str): Markdown内容
        
    Returns:
        str: HTML内容
    """
    
    # HTML模板开始
    html_template_start = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>转换结果</title>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
    <script>
        window.MathJax = {
            tex: {
                inlineMath: [['\\\\(', '\\\\)']],
                displayMath: [['$$', '$$']]
            },
            startup: {
                ready: () => {
                    console.log('MathJax is loaded, but not yet initialized');
                    MathJax.startup.defaultReady();
                    console.log('MathJax is initialized, and the initial typeset is queued');
                }
            },
            chtml: {
                scale: 1.1,
                minScale: 0.8,
                displayAlign: 'center',
                displayIndent: '0'
            }
        };
    </script>
    <style>
        body {
            font-family: 'Times New Roman', serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            text-align: center;
        }
        h2 {
            color: #34495e;
            border-bottom: 2px solid #e74c3c;
            padding-bottom: 5px;
            margin-top: 30px;
        }
        h3 {
            color: #2980b9;
            margin-top: 25px;
        }
        h4 {
            color: #8e44ad;
            margin-top: 20px;
        }
        .math-block {
            margin: 15px 0;
            text-align: center;
            font-size: 1.1em;
            line-height: 1.8;
        }
        
        /* MathJax 数学公式样式优化 */
        .MathJax {
            font-size: 1.1em !important;
        }
        
        .MathJax_Display {
            margin: 1em 0 !important;
            line-height: 1.8 !important;
        }
        
        /* 行内数学公式样式 */
        .MathJax_CHTML {
            line-height: 1.6 !important;
            margin: 0 0.2em !important;
        }
        
        /* 数学公式字符间距优化 */
        mjx-math {
            font-size: 1.1em !important;
            letter-spacing: 0.02em !important;
        }
        
        mjx-mrow {
            margin: 0 0.1em !important;
        }
        .algorithm {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
        }
        ul, ol {
            margin-left: 20px;
        }
        li {
            margin-bottom: 5px;
        }
        strong {
            color: #e74c3c;
        }
        .toc {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 20px;
            margin: 20px 0;
        }
        .toc h2 {
            margin-top: 0;
            border-bottom: none;
        }
        .toc ul {
            list-style-type: none;
            margin-left: 0;
        }
        .toc li {
            margin-bottom: 8px;
        }
        .toc a {
            text-decoration: none;
            color: #2980b9;
        }
        .toc a:hover {
            text-decoration: underline;
        }
        code {
            background-color: #f1f2f6;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        pre {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 15px;
            overflow-x: auto;
        }
        blockquote {
            border-left: 4px solid #3498db;
            margin: 0;
            padding-left: 20px;
            color: #555;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 14px;
        }
        
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        
        th {
            background-color: #f5f5f5;
            font-weight: bold;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        /* 图片样式优化 */
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s ease;
        }
        
        img:hover {
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        /* 图片加载优化 */
        img[src=""] {
            display: none;
        }
        
        @media print {
            body {
                max-width: none;
                margin: 0;
                padding: 15px;
            }
            .toc {
                page-break-after: always;
            }
            h1, h2 {
                page-break-after: avoid;
            }
        }
    </style>
</head>
<body>
'''
    
    # HTML模板结束
    html_template_end = '''
    <script>
        // 页面加载完成后的优化处理
        window.addEventListener('load', function() {
            // 图片懒加载优化
            const images = document.querySelectorAll('img');
            images.forEach(img => {
                if (img.src && !img.complete) {
                    img.addEventListener('load', function() {
                        this.style.opacity = '1';
                    });
                    img.style.opacity = '0.8';
                }
            });
            
            // MathJax渲染优化
            if (window.MathJax && MathJax.typesetPromise) {
                MathJax.typesetPromise().catch(function (err) {
                    console.log('MathJax typeset error: ' + err.message);
                });
            }
        });
        
        // 生成目录
        function generateTOC() {
            const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
            const toc = document.createElement('div');
            toc.className = 'toc';
            
            const tocTitle = document.createElement('h2');
            tocTitle.textContent = '目录';
            toc.appendChild(tocTitle);
            
            const tocList = document.createElement('ul');
            
            headings.forEach((heading, index) => {
                // 为标题添加ID
                if (!heading.id) {
                    heading.id = `heading-${index}`;
                }
                
                const listItem = document.createElement('li');
                const link = document.createElement('a');
                link.href = `#${heading.id}`;
                link.textContent = heading.textContent;
                
                // 根据标题级别设置缩进
                const level = parseInt(heading.tagName.charAt(1));
                listItem.style.marginLeft = `${(level - 1) * 20}px`;
                
                listItem.appendChild(link);
                tocList.appendChild(listItem);
            });
            
            toc.appendChild(tocList);
            
            // 在第一个h1后插入目录
            const firstH1 = document.querySelector('h1');
            if (firstH1 && firstH1.nextSibling) {
                firstH1.parentNode.insertBefore(toc, firstH1.nextSibling);
            }
        }
        
        // 页面加载完成后生成目录
        document.addEventListener('DOMContentLoaded', generateTOC);
    </script>
</body>
</html>'''
    
    # 开始转换
    html_body = convert_md_to_html_body(md_content)
    
    # 组合完整HTML
    full_html = html_template_start + html_body + html_template_end
    
    return full_html

def convert_md_to_html_body(md_content):
    """
    将Markdown内容转换为HTML body内容
    
    Args:
        md_content (str): Markdown内容
        
    Returns:
        str: HTML body内容
    """
    
    lines = md_content.split('\n')
    html_lines = []
    in_code_block = False
    in_math_block = False
    code_language = ''
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 处理代码块
        if line.startswith('```'):
            if not in_code_block:
                in_code_block = True
                code_language = line[3:].strip()
                html_lines.append(f'<pre><code class="language-{code_language}">')
            else:
                in_code_block = False
                html_lines.append('</code></pre>')
            i += 1
            continue
        
        if in_code_block:
            html_lines.append(escape_html(line))
            i += 1
            continue
        
        # 处理数学公式块
        if line.strip().startswith('$$') and line.strip().endswith('$$') and len(line.strip()) > 4:
            # 单行数学公式
            math_content = line.strip()[2:-2]
            html_lines.append(f'<div class="math-block">$${math_content}$$</div>')
            i += 1
            continue
        elif line.strip() == '$$':
            if not in_math_block:
                in_math_block = True
                html_lines.append('<div class="math-block">$$')
            else:
                in_math_block = False
                html_lines.append('$$</div>')
            i += 1
            continue
        
        if in_math_block:
            html_lines.append(line)
            i += 1
            continue
        
        # 处理标题
        if line.startswith('#'):
            level = 0
            for char in line:
                if char == '#':
                    level += 1
                else:
                    break
            
            title_text = line[level:].strip()
            title_id = generate_id(title_text)
            html_lines.append(f'<h{level} id="{title_id}">{process_inline_formatting(title_text)}</h{level}>')
            i += 1
            continue
        
        # 处理列表
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            html_lines.append('<ul>')
            while i < len(lines) and (lines[i].strip().startswith('- ') or lines[i].strip().startswith('* ')):
                item_text = lines[i].strip()[2:]
                html_lines.append(f'<li>{process_inline_formatting(item_text)}</li>')
                i += 1
            html_lines.append('</ul>')
            continue
        
        # 处理表格
        if '|' in line and line.strip().startswith('|') and line.strip().endswith('|'):
            table_lines = []
            # 收集表格行
            while i < len(lines) and '|' in lines[i]:
                table_lines.append(lines[i].strip())
                i += 1
            
            if table_lines:
                html_lines.append('<table>')
                
                # 处理表头
                if len(table_lines) > 0:
                    header_row = table_lines[0]
                    headers = [cell.strip() for cell in header_row.split('|')[1:-1]]  # 去掉首尾空元素
                    html_lines.append('<thead>')
                    html_lines.append('<tr>')
                    for header in headers:
                        html_lines.append(f'<th>{process_inline_formatting(header)}</th>')
                    html_lines.append('</tr>')
                    html_lines.append('</thead>')
                
                # 处理表格数据（跳过分隔行）
                data_start = 2 if len(table_lines) > 1 and '---' in table_lines[1] else 1
                if len(table_lines) > data_start:
                    html_lines.append('<tbody>')
                    for row_line in table_lines[data_start:]:
                        cells = [cell.strip() for cell in row_line.split('|')[1:-1]]  # 去掉首尾空元素
                        html_lines.append('<tr>')
                        for cell in cells:
                            html_lines.append(f'<td>{process_inline_formatting(cell)}</td>')
                        html_lines.append('</tr>')
                    html_lines.append('</tbody>')
                
                html_lines.append('</table>')
            continue
        
        # 处理有序列表
        if re.match(r'^\d+\.\s', line.strip()):
            html_lines.append('<ol>')
            while i < len(lines):
                current_line = lines[i].strip()
                # 如果是有序列表项
                if re.match(r'^\d+\.\s', current_line):
                    item_text = re.sub(r'^\d+\.\s', '', current_line)
                    item_content = [process_inline_formatting(item_text)]
                    i += 1
                    
                    # 处理列表项的缩进内容（包括数学公式）
                    while i < len(lines):
                        next_line = lines[i]
                        # 如果是空行
                        if next_line.strip() == '':
                            i += 1
                            continue
                        # 如果是缩进的内容（以空格开头）
                        elif next_line.startswith('   ') or next_line.startswith('\t'):
                            content = next_line.strip()
                            # 处理数学公式
                            if content.startswith('$$') and content.endswith('$$'):
                                math_content = content[2:-2]
                                item_content.append(f'<div class="math-block">$${math_content}$$</div>')
                            else:
                                item_content.append(process_inline_formatting(content))
                            i += 1
                        # 如果不是缩进内容，退出内容处理
                        else:
                            break
                    
                    html_lines.append(f'<li>{"".join(item_content)}</li>')
                # 如果是空行，跳过并继续检查下一行
                elif current_line == '':
                    i += 1
                    # 检查空行后是否还有有序列表项
                    if i < len(lines) and re.match(r'^\d+\.\s', lines[i].strip()):
                        continue
                    else:
                        break
                # 如果不是有序列表项也不是空行，结束列表
                else:
                    break
            html_lines.append('</ol>')
            continue
        
        # 处理引用
        if line.strip().startswith('>'):
            html_lines.append('<blockquote>')
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_text = lines[i].strip()[1:].strip()
                html_lines.append(f'<p>{process_inline_formatting(quote_text)}</p>')
                i += 1
            html_lines.append('</blockquote>')
            continue
        
        # 处理空行
        if line.strip() == '':
            html_lines.append('')
            i += 1
            continue
        
        # 处理普通段落
        paragraph_lines = []
        while i < len(lines) and lines[i].strip() != '' and not lines[i].startswith('#') and not lines[i].strip().startswith('- ') and not lines[i].strip().startswith('* ') and not re.match(r'^\d+\.\s', lines[i].strip()) and not lines[i].strip().startswith('>') and not lines[i].startswith('```'):
            paragraph_lines.append(lines[i])
            i += 1
        
        if paragraph_lines:
            paragraph_text = ' '.join(paragraph_lines)
            html_lines.append(f'<p>{process_inline_formatting(paragraph_text)}</p>')
    
    return '\n'.join(html_lines)

def process_inline_formatting(text):
    """
    处理行内格式化（粗体、斜体、行内代码、行内数学公式等）
    
    Args:
        text (str): 原始文本
        
    Returns:
        str: 处理后的HTML文本
    """
    
    # 先保护数学公式，避免被其他格式化规则影响
    math_placeholders = {}
    math_counter = 0
    
    # 提取并保护行内数学公式
    def protect_math(match):
        nonlocal math_counter
        placeholder = f'__MATH_PLACEHOLDER_{math_counter}__'
        # 将$包围的数学公式转换为\(\)格式
        math_content = match.group(1)
        math_placeholders[placeholder] = f'\\({math_content}\\)'
        math_counter += 1
        return placeholder
    
    # 更精确的数学公式匹配：包含数学符号、希腊字母、上下标等
    math_pattern = r'\$([^$]*(?:[+\-*/=<>^_{}\\]|\\[a-zA-Z]+|[α-ωΑ-Ω])[^$]*)\$'
    text = re.sub(math_pattern, protect_math, text)
    
    # 处理粗体
    text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
    
    # 处理斜体
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    
    # 处理行内代码
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    
    # 处理图片（在链接之前处理，避免冲突）
    text = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" style="max-width: 100%; height: auto; display: block; margin: 20px auto; border: 1px solid #ddd; border-radius: 5px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />', text)
    
    # 处理链接
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    
    # 恢复数学公式
    for placeholder, math_content in math_placeholders.items():
        text = text.replace(placeholder, math_content)
    
    return text

def generate_id(text):
    """
    为标题生成ID
    
    Args:
        text (str): 标题文本
        
    Returns:
        str: 生成的ID
    """
    
    # 移除特殊字符，保留中文、英文、数字
    clean_text = re.sub(r'[^\w\u4e00-\u9fff]', '-', text)
    clean_text = re.sub(r'-+', '-', clean_text)
    clean_text = clean_text.strip('-')
    
    return clean_text.lower() if clean_text else 'heading'

def escape_html(text):
    """
    转义HTML特殊字符
    
    Args:
        text (str): 原始文本
        
    Returns:
        str: 转义后的文本
    """
    
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&#39;')
    
    return text

def main():
    """
    主函数
    """
    import sys
    
    # 设置文件路径
    current_dir = Path(__file__).parent
    
    # 检查命令行参数
    if len(sys.argv) > 1:
        # 使用命令行参数指定的文件
        md_filename = sys.argv[1]
        if not md_filename.endswith('.md'):
            md_filename += '.md'
        md_file_path = current_dir / md_filename
    else:
        # 默认文件
        md_file_path = current_dir / "model_comparison_report.md"
    
    print("Markdown转HTML转换器")
    print("=" * 50)
    print(f"输入文件：{md_file_path}")
    
    # 检查输入文件是否存在
    if not md_file_path.exists():
        print(f"错误：找不到输入文件 {md_file_path}")
        print("\n可用的Markdown文件：")
        for md_file in current_dir.glob('*.md'):
            print(f"  - {md_file.name}")
        return
    
    # 执行转换
    success = convert_markdown_to_html(str(md_file_path))
    
    if success:
        print("\n转换完成！")
        print("\n使用说明：")
        print("1. 打开生成的HTML文件")
        print("2. 在浏览器中按Ctrl+P（或Cmd+P）打印")
        print("3. 选择'保存为PDF'选项")
        print("4. 调整页面设置（建议A4纸张，包含背景图形）")
        print("5. 保存PDF文件")
    else:
        print("\n转换失败！")

if __name__ == "__main__":
    main()