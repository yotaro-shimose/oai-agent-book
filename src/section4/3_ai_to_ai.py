import asyncio

from agents import Agent, Runner
from dotenv import load_dotenv


async def main():
    load_dotenv()

    # 最初のAIエージェント（質問者）
    questioner = Agent(
        name="質問者",
        instructions="""\
あなたは好奇心旺盛な質問者です。相手のAIに対して、興味深い質問をします。
質問は常に日本語で行い、一度に1つだけ質問してください。
質問のトピックは科学、技術、歴史、文化など幅広い分野から選んでください。
相手の回答に対して、さらに掘り下げた質問をしてください。
""",
        model="gpt-4.1-nano",
    )

    # 2つ目のAIエージェント（回答者）
    responder = Agent(
        name="回答者",
        instructions="""\
あなたは知識豊富な回答者です。質問者からの質問に対して、正確で詳細な回答を提供します。
回答は常に日本語で行い、できるだけ具体的な例や事実を含めてください。
回答の最後には、「他に質問はありますか？」と付け加えてください。
""",
        model="gpt-4.1-mini",
    )

    # 最初の質問
    initial_question = "人工知能の歴史について教えてください。"
    print(f"初期質問: {initial_question}")

    # 現在の質問を初期化
    current_question = initial_question

    # 会話履歴を保存するリスト
    conversation_history = []

    # 会話を5ターン続ける
    for turn in range(5):
        print(f"\n--- ターン {turn + 1} ---")

        # 回答者の応答を取得
        if turn == 0:
            # 初回は直接質問を使用
            responder_result = await Runner.run(
                responder,
                input=current_question,
            )
        else:
            # 2回目以降は会話履歴を文字列として整形して渡す
            conversation_text = "\n".join(
                [
                    f"{'質問者' if i % 2 == 0 else '回答者'}: {msg}"
                    for i, msg in enumerate(conversation_history)
                ]
            )
            responder_result = await Runner.run(
                responder,
                input=f"以下は今までの会話です：\n\n{conversation_text}\n\n最新の質問：\n{current_question}",
            )

        responder_response = responder_result.final_output
        print(f"回答者: {responder_response}")

        # 会話履歴を更新
        conversation_history.append(current_question)
        conversation_history.append(responder_response)

        # 最終ターンなら終了
        if turn == 4:
            break

        # 質問者への指示を準備
        conversation_text = "\n".join(
            [
                f"{'質問者' if i % 2 == 0 else '回答者'}: {msg}"
                for i, msg in enumerate(conversation_history)
            ]
        )

        questioner_prompt = f"""
以下は、あなた(質問者)と回答者の間で行われている会話です。
回答者の最新の回答に基づいて、さらに掘り下げた質問を1つだけ考えてください。

会話履歴:
{conversation_text}

あなたの次の質問を1つだけ書いてください:
"""

        # 質問者の次の質問を取得
        questioner_result = await Runner.run(
            questioner,
            input=questioner_prompt,
        )
        current_question = questioner_result.final_output
        print(f"質問者: {current_question}")


if __name__ == "__main__":
    asyncio.run(main())
