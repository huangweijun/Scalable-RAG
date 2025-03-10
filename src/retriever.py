"""
检索器模块

该模块负责从向量数据库中检索与查询最相关的文本片段。
主要功能:
1. 初始化向量数据库连接
2. 执行语义相似度检索
3. 返回最相关的文档片段
"""

from src.vector_db import VectorDB
from typing import List, Dict

class Retriever:
    """检索器类
    
    负责执行文本检索操作,从向量数据库中找到最相关的文档片段
    
    Attributes:
        vector_db (VectorDB): 向量数据库实例,用于存储和检索文档向量
    """
    
    def __init__(self):
        """初始化检索器
        
        创建向量数据库连接实例
        """
        self.vector_db = VectorDB()

    def retrieve(self, query: str) -> List[Dict]:
        """执行文本检索
        
        将查询文本在向量数据库中进行相似度检索,返回最相关的文档片段
        
        Args:
            query (str): 查询文本
            
        Returns:
            List[Dict]: 检索结果列表,每个结果包含文本内容和相似度分数
            
        示例:
            >>> retriever = Retriever()
            >>> results = retriever.retrieve("如何使用该系统?")
            >>> print(results[0]["text"]) # 打印最相关的文档内容
        """
        return self.vector_db.search(query, top_k=5)