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


class Ingredient(BaseModel):
    name: str
    amount: float
    unit: str  # グラム、個、カップなど


class Recipe(BaseModel):
    title: str
    cuisine_type: str  # 和食、洋食、中華など
    ingredients: list[Ingredient]


# エージェントの作成
recipe_agent = Agent(
    name="レシピアシスタント",
    instructions="""
    あなたは料理レシピを提供するアシスタントです。
    ユーザーが料理について質問したら、その料理のレシピ情報を詳細に提供してください。
    """,
    output_type=Recipe,
    model="gpt-4.1-nano",
)


async def main2():
    load_dotenv()
    # レシピのリクエスト
    recipe_request = "カレーライスのレシピを教えてください。"
    response = await Runner.run(
        recipe_agent,
        input=recipe_request,
    )
    # レシピの出力
    recipe = response.final_output_as(Recipe)
    print(recipe)


if __name__ == "__main__":
    asyncio.run(main2())
