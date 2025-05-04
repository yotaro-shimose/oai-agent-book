import asyncio

from agents import Agent, Runner, WebSearchTool
from pydantic import BaseModel


class PokemonCandidate(BaseModel):
    name: str
    description: str


class PokemonSearchResult(BaseModel):
    candidates: list[PokemonCandidate]


class Pokemon(BaseModel):
    name: str
    type: str
    abilities: list[str]


class PokemonParty(BaseModel):
    description: str
    members: list[Pokemon]


search_agent = Agent(
    name="Pokemon Search Assistant",
    instructions="""\
あなたはポケモン検索エージェントです。
ユーザーがポケモンに関するリクエストをすると、ポケモンの候補を返します。
必ずポケモンはスカーレットバイオレットのポケモンを使用してください。
""",
    model="gpt-4.1",
    tools=[WebSearchTool()],
    output_type=PokemonSearchResult,
)

party_coordinator = Agent(
    name="Party Coordinator",
    instructions="""\
あなたはポケモンパーティーコーディネーターです。
ユーザーがポケモンのパーティーに関するリクエストをすると、ポケモンのパーティーを提案します。
ポケモンはスカーレットバイオレットのポケモンを使用してください。ポケモンの詳細情報に関しては、ポケモン検索エージェントを使用してください。
""",
    model="gpt-4.1",
    tools=[
        search_agent.as_tool(
            tool_name="pokemon_search",
            tool_description="ポケモンの候補を検索するエージェント",
        )
    ],
)


async def main():
    # ユーザーからの質問
    user_input = "まるっこいポケモン１匹、水タイプのかっこいいポケモン１匹、最新の伝説のポケモン１匹を含む６匹のパーティーを作りたいなあ。"
    response = await Runner.run(party_coordinator, input=user_input)
    print(response.final_output)


if __name__ == "__main__":
    asyncio.run(main())
