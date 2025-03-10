"""
文件解析模块

该模块负责解析不同格式的文档文件,将其转换为纯文本格式。
目前支持的文件格式:
- TXT: 纯文本文件
- PDF: PDF文档
- DOCX: Word文档

主要功能:
1. 文件格式识别
2. 文件内容提取
3. 文本格式统一
"""

import os
from PyPDF2 import PdfReader  # 用于解析PDF文件
from docx import Document     # 用于解析DOCX文件

def parse_file(file_path: str) -> str:
    """解析上传的文件内容
    
    根据文件扩展名自动识别文件类型,并使用相应的解析器提取文本内容。
    所有格式最终都会转换为统一的字符串格式。

    Args:
        file_path (str): 待解析文件的路径

    Returns:
        str: 提取的文本内容
        
    示例:
        >>> text = parse_file("example.pdf")
        >>> print(text[:100])  # 打印前100个字符
    """
    # 获取小写的文件扩展名
    ext = os.path.splitext(file_path)[-1].lower()
    text = ""

    # 根据文件类型选择相应的解析方法
    if ext == ".txt":
        # 使用UTF-8编码读取文本文件
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    elif ext == ".pdf":
        # 创建PDF读取器实例
        reader = PdfReader(file_path)
        # 提取每一页的文本并用换行符连接
        # 过滤掉空白页面(extract_text()返回空字符串的页面)
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif ext == ".docx":
        # 创建Word文档读取器实例
        doc = Document(file_path)
        # 提取所有段落的文本并用换行符连接
        text = "\n".join([para.text for para in doc.paragraphs])
    
    return text