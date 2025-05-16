import os
import shutil
import subprocess
import types
from pathlib import Path
from typing import Self

from agents import (
    Agent,
    ModelSettings,
    RunContextWrapper,
    Runner,
    WebSearchTool,
    function_tool,
)
from dotenv import load_dotenv
from loguru import logger
from pydantic import BaseModel


class SandboxContext(BaseModel):
    sandbox: Path
    _old_cwd: Path | None = None

    def __enter__(self):
        """
        ファイル操作のためのサンドボックス環境を作成するコンテキストマネージャー。
        """
        # Create the sandbox directory if it doesn't exist
        self.sandbox.mkdir(parents=True, exist_ok=True)
        self._old_cwd = Path.cwd()  # Store the current working directory
        os.chdir(self.sandbox)  # Change the current working directory to the sandbox
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> None:
        """
        コンテキストマネージャーを終了し、元の作業ディレクトリを復元します。

        Args:
            exc_type: 例外が発生した場合はその例外の型、そうでなければNone。
            exc_val: 例外が発生した場合はその例外のインスタンス、そうでなければNone。
            exc_tb: 例外が発生した場合はそのトレースバック、そうでなければNone。
        """
        assert self._old_cwd is not None, "Old cwd should not be None"
        os.chdir(self._old_cwd)

    @classmethod
    def initialize(cls, sandbox: Path, force: bool = False) -> Self:
        """
        サンドボックスディレクトリを初期化します。

        Args:
            sandbox (Path): サンドボックスディレクトリへのパス。
            force (bool): Trueの場合、新しいディレクトリを作成する前に既存のサンドボックスディレクトリを削除します。
        """
        if sandbox.exists():
            logger.info(f"Sandbox already exists at {sandbox}")
            if not force:
                raise RuntimeError(
                    f"Sandbox already exists at {sandbox}. Use force=True to remove it."
                )
            else:
                logger.info(f"Removing existing sandbox at {sandbox}")
                shutil.rmtree(sandbox)
        sandbox.mkdir(parents=True, exist_ok=True)
        cwd = Path.cwd()
        os.chdir(sandbox)
        ret = subprocess.run(
            ["uv", "init", "--no-workspace"],
        )
        os.chdir(cwd)

        if ret.returncode != 0:
            logger.error(f"Failed to initialize sandbox: {ret.stderr}")
            raise RuntimeError(f"Failed to initialize sandbox: {ret.stderr}")
        logger.info(f"Sandbox initialized at {sandbox}")
        return cls(sandbox=sandbox.resolve())

    @classmethod
    def load(cls, sandbox: Path) -> Self:
        """
        既存のサンドボックスディレクトリを読み込みます。

        Args:
            sandbox (Path): 既存のサンドボックスディレクトリへのパス。
        """
        if not sandbox.exists():
            raise RuntimeError(f"Sandbox does not exist at {sandbox}")
        return cls(sandbox=sandbox.resolve())


@function_tool
def exec_command(
    wrapper: RunContextWrapper[SandboxContext],
    command: str,
) -> str:
    """
    コマンドを実行するツール。
    Args:
        command (str): 実行するコマンド
    """
    context = wrapper.context
    with context:
        logger.info(f"Executing command: {command}")
        # Use subprocess to execute the command in the sandbox
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            env=os.environ.copy() | {"VIRTUAL_ENV": str(context.sandbox / ".venv")},
        )
        if result.returncode != 0:
            logger.error(f"Command failed with error: {result.stderr}")
            return f"Command failed with error: {result.stderr}"
        logger.info(f"Command output: {result.stdout}")
        return result.stdout


@function_tool
def read_file(
    wrapper: RunContextWrapper[SandboxContext],
    path: str,
    start_line: int,
    end_line: int,
) -> str:
    """
    ファイルを読み取るツール。
    ファイルは非常に大きい可能性がるため行数を指定する。
    基本的には0行から500行を指定し、ファイルがさらに大きい場合には行数を指定する。500行以上を同時に読もうとするとエラーになる。
    Args:
        path (str): 読み取るファイルのパス
        start_line (int): 読み取りを開始する行番号（0から始まる）
        end_line (int): 読み取りを終了する行番号（0から始まる）
    """

    context = wrapper.context
    with context:
        file_path = context.sandbox / path
        if not file_path.exists():
            return f"File {file_path} does not exist."
        lines = file_path.read_text(encoding="utf-8").splitlines()
        if start_line < 0 or start_line >= len(lines):
            return "Start line must be greater than or equal to 0 and less than the number of lines in the file."
        if end_line > len(lines):
            end_line = len(lines)
        logger.info(f"Reading lines {start_line} to {end_line} from {file_path}")
        return "\n".join(lines[start_line:end_line])


@function_tool
def write_file(
    wrapper: RunContextWrapper[SandboxContext],
    path: str,
    content: str,
) -> str:
    """
    ファイルに内容を書き込むツール。
    Args:
        path (str): 書き込むファイルのパス
        content (str): 書き込む内容
    """
    context = wrapper.context
    with context:
        file_path = context.sandbox / path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        logger.info(f"Writing to {file_path}")
        return f"File {file_path} written successfully."


@function_tool
def list_dir(wrapper: RunContextWrapper[SandboxContext], path: str) -> str:
    """
    指定されたパスのファイルをリストするツール。
    Args:
        path (str): リストするパス
    """
    context = wrapper.context
    with context:
        file_path = context.sandbox / path
        if not file_path.exists():
            return f"Path {file_path} does not exist."
        if not file_path.is_dir():
            return f"Path {file_path} is not a directory."
        files = [f for f in file_path.iterdir()]
        logger.info(f"Listing files in {file_path}")
        return "\n".join(file.name for file in files)


@function_tool
def ask_user(
    question: str,
):
    """
    ユーザーに質問するツール。
    Args:
        question (str): 質問内容
    """
    return input(f"{question}:\n")


async def main():
    load_dotenv()

    library_search_agent = Agent(
        name="Library Search Agent",
        instructions="""\
あなたは「ライブラリの使い方を調べる」エージェントです。
ユーザーのリクエストに沿ってライブラリの使い方を調べます。
調査にはsearchtoolを使用し、マークダウン形式でレスポンスしてください。
""",
        model="gpt-4.1",
        tools=[WebSearchTool()],
    )

    agent = Agent[SandboxContext](
        name="Coding Assistant",
        instructions="""\
あなたは「コーディングアシスタント」エージェントです。
ユーザーと対話しながらPythonのコードを生成します。

以下のガイドラインにしたがってください。
- 重要：どのような状況においてもツールを呼び出してください
- まずはタスクを理解し、ユーザーに作業内容を確認してください
- プロジェクトは`uv`というパッケージマネージャーツールで管理されています
    - python commandを実行する場合には`uv run file.py`のように実行してください
    - ライブラリのインストールには`uv add package_name`を使用してください
- あなたのすべてのアクションはsandboxディレクトリ内部で実行されます。pathは必ず相対パスを使用してください
- タスクが完了した際は最低でも１度は実行して動作確認をしてください
- 有名でないライブラリを使用する場合にはsearchtoolを利用して使い方を調べてください
- 実行後は必ずユーザーに意見をもとめてください
""",
        model="o4-mini",
        tools=[
            exec_command,
            read_file,
            write_file,
            list_dir,
            ask_user,
            library_search_agent.as_tool(
                tool_name="searchtool",
                tool_description="ライブラリの使い方を調べるためのエージェントです。"
                "LLMエージェントを使ったツールなので調査依頼は自然言語で詳細に行ってください。"
                "とくに調べてほしい内容や目的などを明らかにするとより良い結果が得られます。",
            ),
        ],
        model_settings=ModelSettings(
            tool_choice="required",
        ),
        reset_tool_choice=False,
    )

    # user_input = input("タスクを入力してください:\n")
    user_input = """\
次の競技プログラミングの問題を正解するためのPythonコードを作成してください。

問題文
長さ N の整数列A=(A1,A2,…,A N​
 ) および正整数 
M が与えられます。

A の末尾の要素を削除するという操作を 
0 回以上 
N 回以下行うことで、以下の条件が満たされないようにしたいです。

条件：
A には 
1 以上 
M 以下の整数がすべて含まれている。
必要な操作回数の最小値を求めてください。

なお、本問題の制約下において、操作を 
0 回以上 
N 回以下行うことで上述の条件が満たされないようにすることが必ず可能であることが証明できます。

制約
1≤M≤N≤100
1≤Ai​≤M
入力は全て整数"""

    ret = await Runner.run(
        agent,
        input=user_input,
        context=SandboxContext.initialize(sandbox=Path("agent_sandbox"), force=True),
        max_turns=100,
    )
    print(ret.final_output)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
