"""The “think” tool is better suited for when Claude needs to call complex tools, analyze tool outputs carefully in long chains of tool calls, navigate policy-heavy environments with detailed guidelines, or make sequential decisions where each step builds on previous ones and mistakes are costly. (https://www.anthropic.com/engineering/claude-think-tool)"""

from agents import Agent, Runner, function_tool
from agents.mcp import MCPServerStdio
from dotenv import load_dotenv


@function_tool
def think(thought: str) -> str:
    """
    Use the tool to think about something.
    It will not obtain new information or change the database, but just append the thought to the log.
    Use it when complex reasoning or some cache memory is needed.
    """
    print(f"Thinking: {thought}")
    return thought


async def main():
    load_dotenv()
    async with MCPServerStdio(
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "./mcp_sandbox"],
        }
    ) as server:
        agent = Agent(
            name="Think Assistant",
            instructions="""\
あなたはリサーチアシスタントです。ユーザーの要求にツールを用いて応じます。
あなたは必ず最初と`think`以外のtoolの実行後に`think`ツールを使う必要があります。
タスクの完了まで辛抱強く検討と実行を続けます。

# think toolの使い方
think toolを用いて自分の思考を整理します。典型的なユースケースは以下の通りです。
- 最初にユーザーの質問に答えるための検索の計画を立てる
- 検索結果を観測した後に得られた情報がほしかった情報と一致しているかどうかを検討する
- 計画の見直しに利用する
複雑な課題を解くために何度も積極的に利用してください。

""",
            model="gpt-4.1-mini",
            tools=[think],
            mcp_servers=[server],
        )

        # ユーザーからの質問
        user_input = "機動戦士ガンダムシリーズの代表的な作品５つについてそれぞれのあらすじをまとめてください。それぞれ個別のマークダウンファイルとして保存してください。ファイル名やフォルダ構成はいい感じにしてください。"
        response = await Runner.run(agent, input=user_input, max_turns=30)
        print(response.final_output)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
