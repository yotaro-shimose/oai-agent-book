---
title: "4.2_マルチターンで会話する"
---


前節では基本的なエージェントの作成方法を学びました。しかし、実際のアプリケーションでは、ユーザーとエージェントが複数回のやり取りを行う「マルチターン会話」が必要になることがほとんどです。この節では、OpenAI Agents SDKを使ってマルチターン会話を実装する方法を学びましょう。

## 4.2.1 マルチターン会話の基本

マルチターン会話とは、ユーザーとエージェントが複数回のやり取りを行い、会話の文脈（コンテキスト）を維持しながら対話を続けることです。これにより、エージェントは過去のやり取りを参照して、より適切な応答を提供できるようになります。

OpenAI Agents SDKでは、会話履歴を管理するための方法として、会話履歴の手動管理があります。`to_input_list()`メソッドを使用して会話履歴を取得し、次の呼び出しに渡す方法です。

## 4.2.2 会話履歴の手動管理

会話履歴を手動で管理する方法は、シンプルで柔軟性が高いアプローチです。以下のサンプルコードで、その実装方法を見てみましょう：

```python
import asyncio
from agents import Agent, Runner
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
```

このコードは以下のようなステップで構成されています：

1. 最初の会話ターンを実行し、応答を取得します。
2. `initial_run.to_input_list()`メソッドを使用して、最初の会話ターンの履歴を取得します。
3. 新しいユーザーメッセージを追加して、2回目の会話ターンを実行します。
4. エージェントは前回の会話履歴を参照して、文脈を理解した応答を提供します。

`to_input_list()`メソッドは、会話履歴を以下のような形式のリストとして返します：

```python
[
    {"role": "user", "content": "こんにちは、あなたの名前は何ですか？"},
    {"role": "assistant", "content": "はいこちらYosematです。私の名前はYosematです。今日は良い天気ですね。"}
]
```

このリストに新しいメッセージを追加することで、会話を継続することができます。

```python
initial_run.to_input_list()
    + [
        {
            "role": "user",
            "content": "最後に発言した余計な一言をもう一度言ってください。",
        }
    ]
```
