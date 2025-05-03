from pathlib import Path

from pydantic import BaseModel


class SomeData(BaseModel):
    title: str
    content: str


if __name__ == "__main__":
    # モデルのインスタンスを作成
    data = SomeData(title="Hello", content="World")
    filepath = Path("model.json")

    # JSON文字列をファイルに保存
    filepath.write_text(data.model_dump_json())

    # ファイルからJSON文字列を読み込み
    loaded_data = SomeData.model_validate_json(filepath.read_text())
    print(loaded_data)  # Output: title='Hello' content='World'
