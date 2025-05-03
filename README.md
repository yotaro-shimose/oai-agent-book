# OpenAI Agents SDK 実践ガイド サンプルコード

このリポジトリは「OpenAI Agents SDK 実践ガイド」の書籍に掲載されているサンプルコードを実装したものです。OpenAI Agents SDKを使用したエージェントアプリケーション開発の基本から応用までを学ぶことができます。

## 目次

- [環境構築](#環境構築)
- [プロジェクト構成](#プロジェクト構成)
- [サンプルコードの実行方法](#サンプルコードの実行方法)
- [テストの実行方法](#テストの実行方法)
- [ライセンス](#ライセンス)

## 環境構築

### 前提条件

- Python 3.8以上
- OpenAI APIキー

### インストール手順

1. リポジトリをクローンします：

```bash
git clone https://github.com/yourusername/openai-agents-sdk-examples.git
cd openai-agents-sdk-examples
```

2. 仮想環境を作成し、有効化します：

```bash
python -m venv .venv
source .venv/bin/activate  # Linuxの場合
# または
.venv\Scripts\activate  # Windowsの場合
```

3. 依存パッケージをインストールします：

```bash
pip install -e ".[dev]"
```

4. OpenAI APIキーを設定します：

```bash
export OPENAI_API_KEY=sk-あなたのAPIキー  # Linuxの場合
# または
set OPENAI_API_KEY=sk-あなたのAPIキー  # Windowsの場合
```

または、`.env`ファイルを作成して設定することもできます：

```
OPENAI_API_KEY=sk-あなたのAPIキー
```

## プロジェクト構成

```
.
├── src/
│   └── mylib/
│       ├── agent/
│       │   ├── basic.py        # 基本的なエージェント機能
│       │   ├── multiturn.py    # マルチターン会話機能
│       │   └── output_format.py # 出力形式の指定機能
│       └── utils/
│           ├── context.py      # コンテキスト関連のユーティリティ
│           └── weather.py      # 天気関連のユーティリティ
├── tests/
│   ├── test_chapter2_setup.py  # 2章のテスト
│   ├── test_chapter3_1_agent_creation.py # 3.1節のテスト
│   ├── test_chapter3_2_multiturn.py # 3.2節のテスト
│   └── test_chapter3_3_output_format.py # 3.3節のテスト
├── 2_環境構築/
│   └── 2.1_環境構築.md        # 2章の解説
├── 3_Agents/
│   ├── 3.1_エージェントを作ってみる.md # 3.1節の解説
│   ├── 3.2_マルチターンで会話する.md # 3.2節の解説
│   └── 3.3_出力形式を指定する.md # 3.3節の解説
├── pyproject.toml             # プロジェクト設定
└── README.md                  # このファイル
```

## サンプルコードの実行方法

### 基本的なエージェントの実行

```python
from src.mylib.agent.basic import create_basic_agent, run_agent

# エージェントの作成
agent = create_basic_agent(
    name="アシスタント",
    instructions="あなたは親切なアシスタントです。"
)

# エージェントの実行
response = run_agent(agent, "こんにちは、自己紹介してください。")
print(response)
```

### マルチターン会話の実行

```python
from src.mylib.agent.multiturn import create_conversation_agent, run_multiturn_conversation

# 会話エージェントの作成
agent = create_conversation_agent()

# マルチターン会話の実行
messages = [
    "こんにちは、自己紹介してください。",
    "あなたの趣味は何ですか？",
    "私の名前を覚えていますか？"
]
responses = run_multiturn_conversation(agent, messages)

for i, response in enumerate(responses):
    print(f"質問 {i+1}: {messages[i]}")
    print(f"応答 {i+1}: {response}")
    print("-" * 50)
```

### 構造化出力の使用

```python
from src.mylib.agent.output_format import create_structured_output_agent, WeatherReport

# 構造化出力エージェントの作成
agent = create_structured_output_agent()

# エージェントの実行
from agents import Runner
result = Runner.run_sync(agent, "東京の天気を教えてください。")
weather_data = result.final_output_as(WeatherReport)

print(f"都市: {weather_data.city}")
print(f"天気: {weather_data.condition}")
print(f"気温: {weather_data.temperature}°C")
print(f"湿度: {weather_data.humidity}%")
print(f"風速: {weather_data.wind_speed} m/s")
```

## テストの実行方法

### すべてのテストを実行

```bash
pytest
```

### 特定の章のテストを実行

```bash
# 2章のテストを実行
pytest tests/test_chapter2_setup.py

# 3.1節のテストを実行
pytest tests/test_chapter3_1_agent_creation.py

# 3.2節のテストを実行
pytest tests/test_chapter3_2_multiturn.py

# 3.3節のテストを実行
pytest tests/test_chapter3_3_output_format.py
```

### カバレッジレポートの生成

```bash
pytest --cov=src
```

詳細なテストの実行方法については、[tests/TESTING.md](tests/TESTING.md)を参照してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については[LICENSE](LICENSE)ファイルを参照してください。