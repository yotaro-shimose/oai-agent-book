from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv


async def main():
    load_dotenv()
    async with MCPServerStdio(
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "./mcp_sandbox"],
        }
    ) as server:
        agent = Agent(
            name="Research Assistant",
            instructions="""\
あなたはリサーチアシスタントです。ユーザーの要求にツールを用いて応じます。

""",
            model="gpt-4.1-mini",
            mcp_servers=[server],
        )

        # ユーザーからの質問
        user_input = "server.pyとclient.pyというファイルを作成してください。その中にFastAPIを使ってオウム返しするAPIを実装してください。さらに、client.pyからserver.pyにリクエストを送信してオウム返しの結果を表示するようにしてください。"
        response = await Runner.run(agent, input=user_input, max_turns=30)
        print(response.final_output)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
