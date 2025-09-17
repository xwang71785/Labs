'''
This example demonstrates how to create an agent that uses a custom OpenAI client
for a specific model from thirdparty. It includes the setup of the client, model, and agent,
https://openai.github.io/openai-agents-python/
pip install openai
pip install openai-agents # or `uv add openai-agents`, etc

deepseek-reasoner does not support Function Calling
deepsek dose not support hand-off
'''

import time
import asyncio
import os
from dotenv import load_dotenv

from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled
from agents import FileSearchTool, WebSearchTool, ComputerTool, LocalShellTool

load_dotenv()
# 设置API密钥和基础URL
API_KEY = os.getenv("ALI_API_KEY")
BASE_URL = os.getenv("ALI_BASE_URL")
MODEL_NAME = os.getenv("ALI_MODEL_NAME")

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set EXAMPLE_BASE_URL, EXAMPLE_API_KEY, EXAMPLE_MODEL_NAME via env var or code."
    )

# This example uses a custom provider for a specific agent. Steps:
# 1. Create a custom OpenAI client.
# 2. Create a `Model` that uses the custom client.
# 3. Set the `model` on the Agent.

client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)

llm = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=client,
)

# An alternate approach that would also work:
# PROVIDER = OpenAIProvider(openai_client=client)
# agent = Agent(..., model="some-custom-model")
# Runner.run(agent, ..., run_config=RunConfig(model_provider=PROVIDER))


@function_tool
def get_weather(city: str):
    """Returns the weather for a given city."""
    print(f"[debug] getting weather for {city}")
    return f"The weather in {city} is sunny."

@function_tool
def current_month():
    """Returns the current month as a string."""
    return time.strftime("%B")  

# This agent will use the custom LLM provider'''
agent = Agent(
    name="Assistant",
    instructions="You only respond in haikus.",
    model=llm,  # Use the custom LLM
    tools=[get_weather, current_month],
)

agent_openai = Agent(
    name="Assistant",
    tools=[
        WebSearchTool(),
        FileSearchTool(
            max_num_results=3,
            vector_store_ids=["VECTOR_STORE_ID"],
        ),
    ],
)


# Create a multi-agent handoff system with tool use, 国内模型不太支持
history_tutor_agent = Agent(
    name="历史辅导老师",
    handoff_description="历史问题专家智能体",    # handoff_descriptions为确定交接路由提供了更多上下文。
    instructions="你协助解答历史相关查询。清晰地解释重要事件和背景。",
    model=llm,  # Use the custom LLM
)

math_tutor_agent = Agent(
    name="数学辅导老师",
    handoff_description="数学问题专家智能体",
    instructions="你帮助解决数学问题。在每一步都解释你的推理过程，并包含示例",
    model=llm,  # Use the custom LLM
)

triage_agent = Agent(
    name="分类智能体",
    instructions="你根据用户的家庭作业问题确定使用哪个智能体",
    model=llm,  # Use the custom LLM
    handoffs=[history_tutor_agent, math_tutor_agent]
)

async def main():
    """Run example queries with the agent using the custom model.
    """
#    result = await Runner.run(triage_agent, "who is the first emperor of China?")
#    print(result.final_output)

#    result = await Runner.run(triage_agent, "什么是椭圆")
#    print(result.final_output)

    result = await Runner.run(agent, "What's the month it is ?",)
    print(result.final_output)

    result = await Runner.run(agent, "Which coffee shop should I go to, taking into account my preferences and the weather today in SF?")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
