"""
文本分割模块

该模块负责将长文本切分成较小的文本块,以便于后续的向量化和检索。
主要功能:
1. 使用递归字符分割器进行文本分割
2. 支持设置块大小和重叠长度
3. 返回分割后的文本块列表
"""

from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

def split_text(text: str) -> List[str]:
    """将输入文本分割成小块
    
    使用 LangChain 的 RecursiveCharacterTextSplitter 进行文本分割。
    该分割器会递归地将文本按照不同的分隔符(如换行符、句号、空格等)进行分割,
    确保分割后的文本块在语义上尽可能完整。
    
    Args:
        text (str): 需要分割的原始文本
        
    Returns:
        List[str]: 分割后的文本块列表
        
    示例:
        >>> text = "这是一段很长的文本。需要进行分割。"
        >>> chunks = split_text(text)
        >>> print(len(chunks))  # 输出分割后的块数
    """
    # 创建分割器实例
    # chunk_size: 每个文本块的目标长度(字符数)
    # chunk_overlap: 相邻文本块的重叠长度,用于保持上下文连贯性
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # 设置每块文本大约包含500个字符
        chunk_overlap=50  # 设置50个字符的重叠部分
    )
    
    # 执行分割操作并返回结果
    return splitter.split_text(text)