import asyncio

from agents import Agent, Runner, function_tool


@function_tool
def get_date() -> str:
    """
    Returns the current date in YYYY-MM-DD format.
    """
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%d")


agent = Agent(
    name="Date Assistant",
    instructions="""\
あなたは「今日は何の日」エージェントです。
ユーザーが「今日は何の日」と聞くと今日の日付とその日付に関連する歴史的なイベントを返します。
""",
    model="gpt-4.1-nano",
    tools=[get_date],
)


async def main():
    # ユーザーからの質問
    user_input = "今日は何の日？"
    response = await Runner.run(agent, input=user_input)
    print(response.final_output)


if __name__ == "__main__":
    asyncio.run(main())
