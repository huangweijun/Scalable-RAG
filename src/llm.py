"""
大语言模型调用模块

该模块负责与DeepSeek Chat API进行交互,实现智能问答功能。
主要功能:
1. 初始化并配置DeepSeek Chat模型
2. 处理上下文和问题
3. 调用API生成回答
4. 错误处理
"""

from langchain.chat_models import ChatOpenAI
import os

class LLM:
    """大语言模型封装类
    
    封装了与DeepSeek Chat API交互的主要功能
    
    Attributes:
        api_key (str): DeepSeek API密钥
        model (ChatOpenAI): LangChain封装的DeepSeek Chat模型实例
    """
    
    def __init__(self, api_key=None):
        """初始化DeepSeek Chat API客户端
        
        Args:
            api_key (str, optional): DeepSeek API密钥。如果不提供则从环境变量读取。
        """
        # 优先使用传入的api_key,否则从环境变量获取
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        
        # 初始化DeepSeek Chat模型
        # 使用LangChain提供的ChatOpenAI类
        # 需要配置模型名称、API密钥和API地址
        self.model = ChatOpenAI(
            model_name="deepseek-chat",
            openai_api_key=self.api_key,
            openai_api_base="https://api.deepseek.com"
        )

    def ask(self, question: str, context: str) -> str:
        """调用DeepSeek Chat生成回答
        
        将上下文和问题组合成提示词,调用API生成回答
        
        Args:
            question (str): 用户的问题
            context (str): 相关的上下文信息
            
        Returns:
            str: 模型生成的回答或错误信息
            
        示例:
            >>> llm = LLM()
            >>> answer = llm.ask("Python是什么?", "Python是一种编程语言...")
        """
        # DeepSeek支持的最大上下文长度
        max_context_tokens = 4000
        # 截断过长的上下文,避免超出模型限制
        context = context[:max_context_tokens]

        # 构建提示词模板
        prompt = f"根据以下内容回答问题：\n{context}\n\n问题：{question}"

        try:
            # 调用模型生成回答
            response = self.model.invoke(prompt)
            # 提取回答内容
            # 某些情况下response可能没有content属性,使用str()作为后备方案
            return response.content if hasattr(response, "content") else str(response)
        except ValueError as e:
            # 捕获并处理API调用中的错误
            return f"模型调用失败: {str(e)}"