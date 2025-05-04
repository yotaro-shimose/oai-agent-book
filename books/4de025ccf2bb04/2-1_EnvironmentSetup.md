---
title: "2.1_環境構築"
---

OpenAI Agents SDKを使用するための環境を構築していきましょう。この章ではuvを使ったPythonの仮想環境構築、OpenAI APIキーの取得と設定、そしてAgents SDKのインストールまでを順を追って説明します。

## uvのインストール
uvとは現在のpython環境構築の最先端と思ってください。これまで別々のシステムとして提供されていた以下２つのの機能が、より高機能で高パフォーマンスな形でまとまって提供されています。

- Pythonのバージョン管理（これまではpyenvなどで管理）
- Pythonの依存関係・仮想環境管理（これまではpoetry, pipenv, virtualenvなどで管理）


[uvのインストール](https://docs.astral.sh/uv/getting-started/installation/)を参考にuvをインストールします。

ターミナルで以下のコマンドを打つことでインストールできます。

#### Mac & Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## プロジェクトの作成
適当なフォルダを作ってpythonプロジェクトとして初期化します。


```bash
mkdir my_agents_project
cd my_agents_project
```

次に、仮想環境を作成します：

```bash
uv init
```

この時点ではpyproject.tomlファイルが生成されているでしょう。ファイルを開けばdependenciesが空のリストとして定義されているはずです。

このプロジェクトはOpenAI Agents SDKを利用しますのでここにopenai-agentsへの依存関係を宣言することになるわけですが、コマンドをたたくのがはやいでしょう。

```bash
uv add openai-agents
```

このコマンドを実行した段階で`openai-agents`だけでなくpythonそのものも同時にインストールされます。現在のディレクトリにpythonとそのパッケージが含まれる`.venv`デイレクトリができていれば大丈夫です。

## OpenAI APIアカウントの作成と課金
この本の内容を検証するためにはお金がかかります。この本を書くために何度もサンプルコードを実行しましたが、$5もかかっていません。それでも勉強するのにクレジットカードを登録しなければいけなくなってしまったことは少し残念ですね。
1. [OpenAIのプラットフォーム](https://platform.openai.com/)にアクセスし、アカウントを作成またはログインします。
2. サイドメニューからBillingに移動してクレジットカードを使って$10チャージしてください。

## OpenAI APIキーの取得と設定

OpenAI Agents SDKを使用するには、OpenAIのAPIキーが必要です。まだ持っていない場合は、以下の手順で取得します：

1. [OpenAIのプラットフォーム](https://platform.openai.com/)にアクセスしログインします。
2. 右上の歯車アイコンをクリック
3. サイドメニューからAPI keysをクリック
4. 右上のcreate new secret key

から作成できます。


APIキーを作成したらプロジェクトの直下に`.env`ファイルを作成して、そこに以下のようにAPIキーを記述して保存してください：

OPENAI_API_KEY=sk-あなたのAPIキー

そして、Pythonコード内で`python-dotenv`ライブラリを使用して読み込みます。そのために`python-dotenv`をインストールします。

```bash
uv add python-dotenv
```

プログラムからOpenAIのAPIをコールする前を以下のコードを呼び出してください。
```python
from dotenv import load_dotenv
load_dotenv()
```


## 動作確認

環境構築が完了したら、簡単なコードを書いて動作確認をしましょう。以下のコードを`test_agent.py`というファイル名で保存します：

```python
from agents import Agent, Runner

# エージェントの作成
agent = Agent(
    name="Assistant",
    instructions="あなたは親切なアシスタントです。"
)

# エージェントの実行
result = Runner.run_sync(agent, "プログラミングの再帰に関する俳句を書いてください。")
print(result.final_output)
```

ターミナルで以下のコマンドを実行します：

```bash
python test_agent.py
```

正しく設定されていれば、エージェントからの応答が表示されるはずです。例えば：

```
コードの中のコード
関数が自身を呼び出す
無限の舞い
```

これで、OpenAI Agents SDKを使用するための環境構築は完了です。
