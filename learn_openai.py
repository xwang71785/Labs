"""This example uses a custom provider for a specific agent. Steps:
1. Create a custom OpenAI client.
2. Create a `Model` that uses the custom client.
3. Set the `model` on the Agent.

Note that in this example, we disable tracing under the assumption that you don't have an API key
from platform.openai.com. If you do have one, you can either set the `OPENAI_API_KEY` env var
or call set_tracing_export_api_key() to set a tracing specific key.
"""

import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, Runner, function_tool, set_tracing_disabled

load_dotenv()
BASE_URL = os.getenv("ARK_BASE_URL") or ""
API_KEY = os.getenv("ARK_API_KEY") or ""
MODEL_NAME = os.getenv("ARK_MODEL_NAME") or ""

if not BASE_URL or not API_KEY or not MODEL_NAME:
    raise ValueError(
        "Please set EXAMPLE_BASE_URL, EXAMPLE_API_KEY, EXAMPLE_MODEL_NAME via env var or code."
    )


client = AsyncOpenAI(base_url=BASE_URL, api_key=API_KEY)
set_tracing_disabled(disabled=True)

# Create a custom LLM that uses the custom client
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


async def main():
    # Example 1: Using Agent API to call the custom LLM provider
    agent = Agent(
        name="Assistant",
        instructions="You only respond in haikus.",
        model=llm,  # Use the custom LLM
        tools=[get_weather],
    )

    result = await Runner.run(agent, "What's the weather in Tokyo?")
    print(result.final_output)

    # Example 2: Using the completion API directly
    completion = await client.chat.completions.create(
        # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "你是人工智能助手"},
            {"role": "user", "content": "你好"},
        ],
    )
    print(completion.choices[0].message.content)

    # Example 3: Using the response API directly

if __name__ == "__main__":
    asyncio.run(main())
