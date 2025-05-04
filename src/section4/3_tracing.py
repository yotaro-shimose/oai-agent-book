import asyncio

from agents import Agent, Runner, trace
from dotenv import load_dotenv


async def main():
    load_dotenv()
    yosemat = Agent(
        name="my assistant",
        instructions="""\
あなたはYosematという名前のAIアシスタントです。あなたは日本語を話します。
ユーザーに何を聞かれようとも「はいこちらYosematです。」と答えてから応答します。
最後に余計な一言を言います。
    """,
        model="gpt-4.1-mini",
    )
    with trace("Multi-turn conversation"):
        initial_run = await Runner.run(
            yosemat,
            input="こんにちは、あなたの名前は何ですか？",
        )
        yosemat_response = initial_run.final_output
        print(
            f"一回目の応答: \n{yosemat_response}"
        )  # はいこちらYosematです。私の名前はYosematです。今日は良い天気ですね。

        # 2回目の質問
        second_run = await Runner.run(
            yosemat,
            input=initial_run.to_input_list()
            + [
                {
                    "role": "user",
                    "content": "最後に発言した余計な一言をもう一度言ってください。",
                }
            ],
        )
        yosemat_response = second_run.final_output
        print(
            f"二回目の応答: \n{yosemat_response}"
        )  # はいこちらYosematです。今日は良い天気ですね。コーヒーでも飲みたくなりますね。


if __name__ == "__main__":
    asyncio.run(main())
