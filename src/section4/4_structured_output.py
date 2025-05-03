import asyncio

from agents import Agent, Runner
from dotenv import load_dotenv
from pydantic import BaseModel


class Country(BaseModel):
    name: str
    capital: str


async def main():
    load_dotenv()
    agent = Agent(
        name="assistant",
        instructions="""\
あなたは国名と首都名を知っているAIアシスタントです。ユーザーに国について質問されると、国名と首都名を答えます。
    """,
        output_type=Country,
        model="gpt-4.1-nano",
    )
    response = await Runner.run(
        agent,
        input="世界で一番人口が多い国はどこですか？",
    )
    print(response.final_output_as(Country))


if __name__ == "__main__":
    asyncio.run(main())
