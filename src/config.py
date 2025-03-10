"""
配置文件模块

该模块负责管理系统的所有配置参数,通过环境变量的方式实现配置的灵活管理。
主要包含:
1. API密钥配置 
2. 模型配置
3. 文件路径配置
4. 系统参数配置
"""

import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
# 这样可以避免敏感信息直接写在代码中
load_dotenv()

class Config:
    """配置类
    
    存储所有系统配置参数的类,所有属性都是类属性,方便全局访问
    
    Attributes:
        DEEPSEEK_API_KEY (str): DeepSeek API密钥,用于访问大语言模型服务
        EMBEDDING_MODEL (str): 文本向量化模型名称,默认使用OpenAI的ada模型
        VECTOR_DB_PATH (str): 向量数据库存储路径
        LLM_MODEL (str): 大语言模型名称,默认使用DeepSeek Chat
        FILE_STORAGE_PATH (str): 上传文件存储路径
        TOKENIZERS_PARALLELISM (str): 是否启用tokenizer并行处理
    """
    
    # API配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # 从环境变量获取API密钥
    
    # 模型配置
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")  # 文本向量化模型
    LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")  # 大语言模型
    
    # 路径配置 
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH", "./data/vector_store")  # 向量数据库路径
    FILE_STORAGE_PATH = os.getenv("FILE_STORAGE_PATH", "./data/uploads")  # 文件上传路径
    
    # 系统配置
    TOKENIZERS_PARALLELISM = os.getenv("TOKENIZERS_PARALLELISM", "false")  # tokenizer并行设置