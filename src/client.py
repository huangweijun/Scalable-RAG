"""
文档智能问答系统的命令行客户端
提供了与后端 API 交互的主要功能，包括:
- 智能问答查询
- 文件上传
- 文档检索
"""

import requests
import json
import os

class APIClient:
    """API 客户端类
    
    负责与后端服务进行 HTTP 通信，封装了主要的 API 调用方法
    
    Attributes:
        base_url (str): API 服务的基础 URL,默认为本地测试环境
    """
    
    def __init__(self, base_url="http://localhost:8000"):
        """初始化 API 客户端
        
        Args:
            base_url (str): API 服务的基础 URL
        """
        self.base_url = base_url

    def query(self, question):
        """发送智能问答查询请求并格式化输出结果
        
        调用 /query/ 接口获取 AI 回答和相关文档
        
        Args:
            question (str): 用户的问题
        """
        response = requests.get(f"{self.base_url}/query/", params={"q": question})
        if response.status_code == 200:
            data = response.json()
            # 按照固定格式打印查询结果
            print("\n**Query:**\n")
            print(f"> {data['query']}\n")

            print("\n**Answer:**\n")
            print(data["answer"])

            print("\n**Retrieved Documents:**\n")
            print(data["retrieved"])
        else:
            print("❌ 查询失败:", response.status_code, response.text)

    def retrieve_only(self, question):
        """仅从向量数据库检索相关文档
        
        调用 /retrieve/ 接口获取相关文档，不生成 AI 回答
        
        Args:
            question (str): 检索关键词
        """
        response = requests.get(f"{self.base_url}/retrieve/", params={"q": question})
        if response.status_code == 200:
            data = response.json()
            print("\n**Query:**\n")
            print(f"> {data['query']}\n")

            print("\n**Retrieved Documents:**\n")
            print(data["retrieved"])
        else:
            print("❌ 召回失败:", response.status_code, response.text)

    def upload_file(self, file_path):
        """上传文件到系统
        
        调用 /upload/ 接口上传文件并向量化存储
        
        Args:
            file_path (str): 要上传的文件路径
        """
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"❌ 文件 '{file_path}' 不存在")
            return

        # 打开文件并上传
        with open(file_path, "rb") as file:
            files = {"file": file}
            response = requests.post(f"{self.base_url}/upload/", files=files)

        if response.status_code == 200:
            print("✅ 文件上传成功！")
            print(response.json())
        else:
            print("❌ 上传失败:", response.status_code, response.text)

def main():
    """主函数，提供交互式命令行界面
    
    循环显示菜单并处理用户输入，直到用户选择退出
    """
    # 初始化客户端
    client = APIClient()
    
    # 主循环
    while True:
        # 显示操作菜单
        print("\n🔹 请选择操作：")
        print("1️⃣  查询 (Query)")
        print("2️⃣  上传文件 (Upload)")
        print("3️⃣  仅召回数据库内容 (Retrieve Only)")
        print("4️⃣  退出 (Exit)")

        # 获取用户输入
        choice = input("请输入选项 (1/2/3/4): ").strip()
        
        # 根据用户选择执行相应操作
        if choice == "1":
            question = input("请输入您的查询: ")
            client.query(question)
        elif choice == "2":
            file_path = input("请输入要上传的文件路径: ")
            client.upload_file(file_path)
        elif choice == "3":
            question = input("请输入您的查询: ")
            client.retrieve_only(question)
        elif choice == "4":
            print("👋 退出客户端")
            break
        else:
            print("❌ 无效选项，请重新输入")

if __name__ == "__main__":
    main()