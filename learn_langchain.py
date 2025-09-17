'''
AI Agent with LangChain: Weather and Stock Price Query
This script demonstrates how to create an AI agent using LangChain that can query weather and stock prices
with customized LLMs through ChatOpenAI.
also demonstrates creating a chain that ensures output is a pure string using StrOutputParser.
'''
import os
import json
import requests
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableSequence
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    # Step 1.构建请求
    url = "https://api.openweathermap.org/data/2.5/weather"

    # Step 2.设置查询参数
    params = {
        "q": city,                     # 输入城市名称
        "appid": os.getenv("OPENWEATHER_API_KEY"),    # 输入API key
        "units": "metric",            # 使用摄氏度而不是华氏度
        "lang":"zh_cn"                # 输出语言为简体中文
    }

    # Step 3.发送GET请求
    response = requests.get(url, params=params, timeout=5)
    
    # Step 4.解析响应
    data = response.json()
    return json.dumps(data)

@tool
def get_stock_price(symbol):
    """获取股票价格"""
    # 模拟股票API调用
    return {
        "symbol": symbol,
        "price": 150.25,
        "change": "+2.5%"
    }


# 设置API密钥和基础URL
API_KEY = os.getenv("ALI_API_KEY")
BASE_URL = os.getenv("ALI_BASE_URL")
MODEL_NAME = os.getenv("ALI_MODEL_NAME")

# 创建LLM
llm = ChatOpenAI(
    model=MODEL_NAME,
    openai_api_key=API_KEY,
    openai_api_base=BASE_URL,
)

# 工具列表
tools = [get_weather, get_stock_price]

# 创建代理
prompt = hub.pull("hwchase17/react")
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, max_iterations=3)

def create_doubao_chain():
    """
    创建调用豆包大模型的链,并使用StrOutputParser确保输出为纯字符串
    
    参数:
        api_key: 豆包API密钥
        base_url: 豆包API的基础URL
    """
    # 1. 定义提示模板
    prompt_template = ChatPromptTemplate.from_template("请回答以下问题: {question}")

    # 2. 定义语言模型

    # 3. 定义输出解析器（将模型输出转换为纯字符串）
    output_parser = StrOutputParser()

    # 4. 构建链：提示模板 -> 模型 -> 输出解析器
    chain = RunnableSequence(
        prompt_template | llm | output_parser
    )

    return chain


def main():
    # 运行代理
    # result = agent_executor.invoke({"input": "how is the weather in shanghai today?"})
    # print(result['output'])

    # 查询股票价格
    stock_result = agent_executor.invoke({"input": "查询苹果公司的股票价格"})
    print(stock_result['output'])

    # 创建链
    doubao_chain = create_doubao_chain()
    # 测试问题
    question = "什么是自然语言处理？用简洁的语言解释。"
    # 调用链获取结果（已确保为纯字符串）
    result = doubao_chain.invoke({"question": question})
    # 输出结果及类型验证
    print("模型输出结果:")
    print(result)
    # 证明此处的llm就是langchain中的model
    # chain的invoke传入的是字典而model的invoke传入的是字符串
    question2 = "请用一句话解释什么是机器学习。"
    result2 = llm.invoke(question2)
    print(f"模型输出结果:{result2.content}")

if __name__ == "__main__":
    main()
