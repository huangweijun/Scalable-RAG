"""
文本向量化模块

该模块负责将文本转换为向量表示，主要功能：
1. 加载预训练的Sentence Transformer模型
2. 将输入文本转换为向量形式
3. 支持文本相似度计算和语义检索

使用的模型:
- all-MiniLM-L6-v2: 一个轻量级但效果不错的开源模型
- 384维向量输出
- 支持多语言
"""

import os
from sentence_transformers import SentenceTransformer
from typing import List

# 禁用 TensorFlow,避免不必要的依赖加载
os.environ["DISABLE_TRANSFORMERS_TF"] = "1"

# 初始化sentence-transformers模型
# all-MiniLM-L6-v2是一个效果和性能均衡的模型
# 也可以使用其他模型如paraphrase-multilingual-MiniLM-L12-v2等
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str) -> List[float]:
    """将文本转换为向量表示
    
    使用预训练模型将输入文本编码为固定维度的向量。
    这个向量可以用于后续的相似度计算和检索。

    Args:
        text (str): 需要向量化的输入文本

    Returns:
        List[float]: 文本对应的向量表示,384维浮点数列表
    """
    # encode()方法将文本转换为numpy数组,tolist()转为Python列表
    return embedding_model.encode(text).tolist()