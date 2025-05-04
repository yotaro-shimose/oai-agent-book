---
title: "4.1_エージェントを作ってみる"
---


前章で環境構築と基礎知識を学んだので、いよいよOpenAI Agents SDKを使ってエージェントを作成していきましょう。この章では、基本的なエージェントの作成方法を学びます。

## 4.1.1 エージェントの基本構造

OpenAI Agents SDKでは、`Agent`クラスがエージェントの中核となります。エージェントは大規模言語モデル（LLM）に指示（instructions）を与えることで、特定の役割や振る舞いを持つアシスタントとして機能します。

最もシンプルなエージェントは、以下のように作成できます：

```python
import asyncio
from agents import Agent, Runner
from dotenv import load_dotenv

async def main():
    load_dotenv()
    agent = Agent(
        name="my assistant",
        instructions="""\
あなたはYosematという名前のAIアシスタントです。あなたは日本語を話します。
ユーザーに何を聞かれようとも「はいこちらYosematです。」と答えてから応答します。
最後に余計な一言を言います。
    """,
        model="gpt-4.1-nano",
    )
    response = await Runner.run(
        agent,
        input="こんにちは、あなたの名前は何ですか？",
    )
    print(response.final_output)
    # 出力例: はいこちらYosematです。私の名前はYosematです。今日はどんなお手伝いをしましょうか？宇宙も広いですよね。

if __name__ == "__main__":
    asyncio.run(main())
```

このコードでは、以下の重要な要素があります：

1. **環境変数の読み込み**: `load_dotenv()`を使用して、`.env`ファイルから環境変数（OpenAI APIキーなど）を読み込みます。
2. **エージェントの作成**: `Agent`クラスを使用してエージェントを作成します。
   - `name`: エージェントの名前
   - `instructions`: エージェントへの指示（システムプロンプト）
   - `model`: 使用するLLMモデル
3. **エージェントの実行**: `Runner.run()`メソッドを使用して非同期でエージェントを実行します。
4. **結果の取得**: `response.final_output`で最終的な応答を取得します。

## 4.1.2 エージェントの設定オプション

エージェントを作成する際には、様々な設定オプションを指定できます。主な設定項目は以下の通りです：

1. **name**: エージェントの名前
2. **instructions**: エージェントへの指示（システムプロンプト）
3. **model**: 使用するLLMモデル（例: "gpt-4.1-nano", "gpt-4.1-mini", "gpt-4o"など）
4. **tools**: エージェントが使用できるツールのリスト
5. **output_type**: エージェントの出力の型（構造化出力を使用する場合）

### モデルの選択

OpenAI Agents SDKでは、様々なモデルを使用できます。モデルの選択は、エージェントの能力と応答速度、コストのバランスを考慮して行います。

```python
# 軽量モデルを使用したエージェント
agent_nano = Agent(
    name="軽量アシスタント",
    instructions="あなたは簡潔な応答を提供するアシスタントです。",
    model="gpt-4.1-nano",  # 軽量で高速なモデル
)

# 高性能モデルを使用したエージェント
agent_premium = Agent(
    name="高性能アシスタント",
    instructions="あなたは詳細な応答を提供するアシスタントです。",
    model="gpt-4.1",  # より高性能なモデル
)
```

### 指示（Instructions）の設計

エージェントの振る舞いを決定する最も重要な要素はinstructionsです。システムプロンプトとも呼ばれます。システムプロンプトは、エージェントの役割、応答スタイル、制約条件などを定義します。


## 4.1.3 エージェントの実行方法

エージェントを実行するには、主に2つの方法があります：

1. **非同期実行**: `Runner.run()`メソッドを使用します。Webアプリケーションなど、非同期処理が必要な場合に適しています。
2. **同期実行**: `Runner.run_sync()`メソッドを使用します。シンプルなスクリプトや対話型環境で便利です。エージェント開発では基本的に使う必要はないでしょう。

### 非同期実行の例

```python
import asyncio
from agents import Agent, Runner

async def main():
    agent = Agent(
        name="アシスタント",
        instructions="あなたは親切なアシスタントです。"
    )
    
    result = await Runner.run(agent, "こんにちは、自己紹介してください。")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
```

### 同期実行の例

```python
from agents import Agent, Runner

agent = Agent(
    name="アシスタント",
    instructions="あなたは親切なアシスタントです。"
)

result = Runner.run_sync(agent, "こんにちは、自己紹介してください。")
print(result.final_output)
```

## 4.1.4 応答の取得と処理

エージェントからの応答は、`Runner.run()`または`Runner.run_sync()`メソッドの戻り値として取得できます。この戻り値には、以下のような情報が含まれています：

- **final_output**: エージェントの最終的な応答オブジェクト。デフォルトで`str`がかえってくる。
- **to_input_list()**: 会話履歴をメッセージリストとして取得するメソッド

```python
response = await Runner.run(agent, "こんにちは")
print(response.final_output)  # エージェントの応答テキスト

# 会話履歴の取得
message_history = response.to_input_list()
print(message_history)  # [{"role": "user", "content": "こんにちは"}, {"role": "assistant", "content": "..."}]
```

## まとめ

この章では、OpenAI Agents SDKを使った基本的なエージェントの作成方法を学びました。エージェントの基本構造、設定オプション、実行方法、そして応答の取得と処理について説明しました。

次の章では、エージェントとのマルチターン会話の実装方法について学んでいきます。マルチターン会話を実装することで、より自然で継続的な対話が可能になります。