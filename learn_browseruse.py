"""
uv pip install browser-use
uv run playwright install
the ARK model is not capable of generate action plans with browser_use, so we use the ALI model
"""

import os
import asyncio
from browser_use.llm import ChatOpenAI
from browser_use import Agent
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("ALI_API_KEY")
BASE_URL = os.getenv("ALI_BASE_URL")
MODEL_NAME = os.getenv("ALI_MODEL_NAME")

llm = ChatOpenAI(
    base_url=BASE_URL,
    model=MODEL_NAME,
    api_key=API_KEY,)

async def main():
    """Main function to run the agent."""
    agent = Agent(
        task="Compare the price of gpt-4o and DeepSeek-V3",
        llm=llm,
        #browser="firefox",
    )
    result = await agent.run()
    print(result)

if __name__ == "__main__":
    # Run the main function in an asyncio event loop
    asyncio.run(main())
