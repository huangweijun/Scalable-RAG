

 # Scalable-RAG
 
 **Scalable-RAG** 是一个可扩展的 **RAG（Retrieval-Augmented Generation）** 解决方案，集成了 DeepSeek 和 LangChain，支持文件上传、内容召回、问答等功能。
 
 ## 🚀 功能介绍
 - 📂 **文件上传**：支持 PDF、TXT 等格式，自动解析并存储到向量数据库。
 - 🔍 **内容召回**：基于用户查询，从数据库检索最相关的文档片段。
 - 💬 **智能问答**：调用 DeepSeek 生成回答，并格式化为 Markdown 。
 - 📚 **支持持久化存储**：基于 `ChromaDB` 存储和管理嵌入向量。
 
 ## 📦 安装 & 依赖
 **克隆项目**
 ```bash
 git clone -b V1 https://github.com/your-username/Scalable-RAG.git
 cd Scalable-RAG
 ```
 
 **安装依赖**
 ```bash
 pip install -r requirements.txt
 ```
 
 **配置 `.env`**
 ```ini
 DEEPSEEK_API_KEY=your_deepseek_api_key_here
 ```
 
 ## 🚀 启动服务
 **运行 FastAPI**
 ```bash
 uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
 ```

 ## 🛠️ 部署模型
 
 **1️⃣ 下载模型**
 如果你使用的是 **本地 LLM（如 Llama 2）**，请先下载适配的模型文件：
 ```bash
 mkdir -p models/
 wget -P models/ https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf
 ```
 如果你使用 **DeepSeek API**，请确保你已经正确配置了 API Key。
 
 **2️⃣ 配置 `.env`**
 在项目根目录创建 `.env` 文件，并添加以下内容：
 ```ini
 DEEPSEEK_API_KEY=your_deepseek_api_key_here
 ```
 
 **3️⃣ 修改 `llm.py` 以选择本地模型或 API**
 确保 `llm.py` 中正确设置本地模型路径或 API 方式：
 ```python
 from langchain.llms import LlamaCpp
 
 class LLM:
     def __init__(self, model_path="./models/llama-2-7b.Q4_K_M.gguf"):
         self.model = LlamaCpp(model_path=model_path, n_ctx=1024)
 
     def ask(self, question: str, context: str) -> str:
         prompt = f"根据以下内容回答问题：\n{context}\n\n问题：{question}"
         return self.model.invoke(prompt)
 ```
 
 **4️⃣ 启动 FastAPI 服务**
 ```bash
 uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
 ```
 
 ## 🔎 API 使用
 **1️⃣ 查询内容**
 ```bash
 curl -G --data-urlencode "q=你的问题" "http://localhost:8000/query/"
 ```
 
 **2️⃣ 上传文件**
 ```bash
 curl -X POST "http://localhost:8000/upload/" -F "file=@path/to/your/file.pdf"
 ```
 
 **3️⃣ 仅召回数据库内容**
 ```bash
 curl -G --data-urlencode "q=你的问题" "http://localhost:8000/retrieve/"
 ```
 
 ## 📌 分支管理
 - `main`：主分支，稳定版
 - `V1`：当前开发版本
 
 ## 🤝 贡献指南
 欢迎提交 Issue 和 PR ！