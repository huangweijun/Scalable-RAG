"""
FastAPI 文档智能问答系统
该系统实现了文档上传、向量化存储、智能检索和问答等功能

主要功能：
1. 文件上传和处理
2. 文本向量化和存储
3. 智能检索
4. AI 问答
"""

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from markdownify import markdownify
import os
from typing import List, Dict, Any
from src.file_parser import parse_file
from src.text_splitter import split_text
from src.embedding import embed_text
from src.vector_db import VectorDB
from src.config import Config
from src.llm import LLM
from src.retriever import Retriever

# 初始化 FastAPI 应用
app = FastAPI(
    title="文档智能问答系统",
    description="基于向量检索和大语言模型的智能问答系统",
    version="1.0.0"
)

# 初始化系统组件
vector_db = VectorDB()  # 向量数据库实例
llm = LLM(api_key=Config.DEEPSEEK_API_KEY)  # 大语言模型实例
retriever = Retriever()  # 检索器实例

# 定义常量
UPLOAD_DIR = "./data/uploads"  # 文件上传目录

@app.post("/upload/", 
    response_model=Dict[str, str],
    summary="上传文件接口",
    description="接收文件上传，处理文件内容并存储到向量数据库"
)
async def upload_file(file: UploadFile = File(...)) -> Dict[str, str]:
    """
    处理文件上传的端点

    处理流程：
    1. 保存上传的文件
    2. 解析文件内容
    3. 分割文本
    4. 计算文本向量
    5. 存储到向量数据库

    Args:
        file (UploadFile): 上传的文件对象

    Returns:
        Dict[str, str]: 包含处理结果的字典
    """
    # 确保上传目录存在
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # 构建文件保存路径
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # 保存上传的文件
    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"文件保存失败: {str(e)}"}
        )

    # 处理文件内容
    try:
        # 解析文件内容
        text = parse_file(file_path)
        # 分割文本为较小的块
        chunks = split_text(text)
        
        # 处理每个文本块
        for chunk in chunks:
            # 计算文本的向量表示
            embedding = embed_text(chunk)
            # 将文本及其向量存入数据库
            vector_db.add(chunk, embedding)
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"文件处理失败: {str(e)}"}
        )

    return {
        "filename": file.filename, 
        "message": "文件上传和处理成功"
    }

@app.get("/query/",
    response_model=Dict[str, str],
    summary="智能问答接口",
    description="根据用户提问检索相关文档并生成答案"
)
async def query(q: str) -> Dict[str, str]:
    """
    处理用户查询的端点

    处理流程：
    1. 检索相关文档
    2. 使用大语言模型生成答案
    3. 格式化返回结果

    Args:
        q (str): 用户的问题

    Returns:
        Dict[str, str]: 包含问题、答案和检索内容的字典
    """
    # 检索相关文档
    docs = retriever.retrieve(q)
    
    # 处理未找到相关内容的情况
    if not docs:
        return JSONResponse(content={
            "query": q,
            "answer": "没有找到相关内容。"
        })

    # 处理检索到的文档
    retrieved_md = "\n\n".join([
        markdownify(text) for text in docs
    ])  # 将检索内容转换为Markdown格式
    
    # 使用LLM生成答案
    answer = llm.ask(q, docs)
    
    # 格式化答案
    answer_md = markdownify(answer.strip()).replace("\n", "\n\n")

    return JSONResponse(content={
        "query": q,
        "answer": answer_md,
        "retrieved": retrieved_md
    })

@app.get("/retrieve/",
    response_model=Dict[str, str],
    summary="文档检索接口",
    description="仅检索相关文档，不生成AI回答"
)
async def retrieve_only(q: str) -> Dict[str, str]:
    """
    仅执行文档检索的端点

    处理流程：
    1. 检索相关文档
    2. 格式化检索结果

    Args:
        q (str): 检索关键词

    Returns:
        Dict[str, str]: 包含检索内容的字典
    """
    # 执行检索
    docs = retriever.retrieve(q)
    
    # 处理未找到相关内容的情况
    if not docs:
        return JSONResponse(content={
            "query": q,
            "retrieved": "没有找到相关内容。"
        })

    # 格式化检索结果
    retrieved_md = "\n\n".join([
        markdownify(text) for text in docs
    ])

    return JSONResponse(content={
        "query": q,
        "retrieved": retrieved_md
    })