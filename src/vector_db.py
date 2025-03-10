"""
向量数据库模块

该模块负责文本向量的存储和检索功能。
主要功能:
1. 使用 HuggingFace 的 sentence-transformers 模型进行文本向量化
2. 使用 Chroma 向量数据库存储文本向量
3. 提供向量相似度检索功能
"""

from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

class VectorDB:
    """向量数据库类
    
    负责文本的向量化存储和检索
    
    Attributes:
        embeddings (HuggingFaceEmbeddings): 文本向量化模型
        vector_store (Chroma): 向量数据库实例
    """
    
    def __init__(self, persist_directory="./data/vector_store"):
        """初始化向量数据库
        
        Args:
            persist_directory (str): 向量数据库持久化存储路径
        """
        # 初始化文本向量化模型,使用轻量级的 all-MiniLM-L6-v2 模型
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # 初始化 Chroma 向量数据库
        self.vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embeddings
        )

    def add(self, text):
        """存储文本到向量数据库
        
        将输入文本转换为向量并存储
        
        Args:
            text (str): 需要存储的文本内容
        """
        self.vector_store.add_texts([text])

    def search(self, query, top_k=5):
        """检索最相似的文本
        
        根据查询文本检索向量数据库中最相似的文档
        
        Args:
            query (str): 查询文本
            top_k (int): 返回结果的数量
            
        Returns:
            List[str]: 检索到的文本内容列表
        """
        # 执行相似度检索
        docs = self.vector_store.similarity_search(query, k=top_k)
        # 提取文档内容并返回
        return [doc.page_content for doc in docs]