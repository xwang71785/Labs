'''
AI Agent with LangChain: Weather and Stock Price Query
This script demonstrates how to create an AI agent using LangChain that can query weather and stock prices
with customized LLMs instead of OpenAI's chat-gpt
'''
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

@tool
def get_weather(city: str) -> str:
    """获取指定城市的天气信息"""
    # 这里应该调用真实的天气API
    # 示例返回
    return f"{city}的天气：晴天，温度25°C，湿度60%"

@tool
def get_stock_price(symbol):
    """获取股票价格"""
    # 模拟股票API调用
    return {
        "symbol": symbol,
        "price": 150.25,
        "change": "+2.5%"
    }

load_dotenv()
# 设置API密钥和基础URL
API_KEY = os.getenv("GLM_API_KEY")
BASE_URL = os.getenv("GLM_BASE_URL")
MODEL_NAME = os.getenv("GLM_MODEL_NAME")

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

# 使用代理
result = agent_executor.invoke({"input": "北京今天天气怎么样？然后帮我查询股票价格，股票代码是000001"})
print(result['output'])
