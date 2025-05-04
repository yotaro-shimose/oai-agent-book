---
title: "3.1_Pydantic"
---

## はじめに

エージェント開発において、データの検証と型安全性は非常に重要です。OpenAI Agents SDKでは、Pydanticというライブラリを使用してデータモデルを定義します。この章では、Pydanticの基本的な使い方から応用までを学びます。

## 3.1.1 Pydanticとは

Pydanticは、Pythonのデータバリデーションと設定管理のためのライブラリです。型アノテーションを使用してデータモデルを定義し、実行時に型チェックとバリデーションを行います。

Pydanticの主な特徴は以下の通りです：

- データモデルの定義
- 型アノテーションに基づくデータバリデーション
- JSON/dict形式との相互変換

## 3.1.2 基本的な使い方

Pydanticの基本的な使い方を見ていきましょう。まず、通常のPythonクラスとPydanticモデルの違いを比較します。

```python
from pydantic import BaseModel


class Person:
    def __init__(self, name: str):
        self.name = name

    def greet(self) -> str:
        return f"Hello, my name is {self.name}."


class PydanticPerson(BaseModel):
    name: str

    def greet(self) -> str:
        return f"Hello, my name is {self.name}."


if __name__ == "__main__":
    person = Person("Alice")
    print(person.greet())  # Output: Hello, my name is Alice.

    pydantic_person = PydanticPerson(name="Bob")
    print(pydantic_person.greet())  # Output: Hello, my name is Bob.

    # 不適切なデータを渡すとエラーが発生
    invalid_person = PydanticPerson(name=123)  # ValidationError
```

通常のPythonクラス（`Person`）とPydanticモデル（`PydanticPerson`）の主な違いは以下の点です：

1. Pydanticモデルは`BaseModel`を継承します
2. 属性を型アノテーションで定義します（`name: str`）
3. `__init__`メソッドを明示的に定義する必要がありません
4. 不適切なデータ型（例：nameに数値）を渡すとバリデーションエラーが発生します

## 3.1.3 JSON/dict変換

Pydanticの大きな利点の一つは、モデルとJSON/dict形式の間で簡単に変換できることです。これはAPIやファイル入出力などでデータをやり取りする際に非常に便利です。

```python
from pydantic import BaseModel


class PydanticPerson(BaseModel):
    name: str

    def greet(self) -> str:
        return f"Hello, my name is {self.name}."


if __name__ == "__main__":
    # PydanticのモデルはdictやJSON文字列と相互変換できる
    pydantic_person = PydanticPerson(name="Bob")

    # dict型に変換
    dict_obj = pydantic_person.model_dump()
    print(dict_obj)  # dict型の{"name": "Bob"}
    # JSON文字列に変換
    json_str = pydantic_person.model_dump_json()
    print(json_str)  # str型の'{"name": "Bob"}'

    # JSON文字列をdict型に変換
    json_str = '{"name": "Bob"}'
    dict_obj = PydanticPerson.model_validate_json(json_str)
    print(dict_obj)  # PydanticPerson(name='Bob')
    # dict型をJSON文字列に変換
    dict_obj = {"name": "Bob"}
    json_str = PydanticPerson.model_validate(dict_obj)
    print(json_str)  # PydanticPerson(name='Bob')
```

主なメソッドは以下の通りです：

- `model_dump()`: Pydanticモデルをdict型に変換
- `model_dump_json()`: PydanticモデルをJSON文字列に変換
- `model_validate_json()`: JSON文字列からPydanticモデルに変換
- `model_validate()`: dict型からPydanticモデルに変換

## 3.1.4 ネストされたモデル

複雑なデータ構造を表現するために、Pydanticではモデルをネストすることができます。

```python
from pydantic import BaseModel


class InnerModel(BaseModel):
    name: str
    age: int


class NestedModel(BaseModel):
    inner: InnerModel


if __name__ == "__main__":
    # ネストされたモデルのインスタンスを作成
    inner_instance = InnerModel(name="Alice", age=30)
    nested_instance = NestedModel(inner=inner_instance)
    print(nested_instance)  # Output: inner=InnerModel(name='Alice', age=30)

    # ネストされたdictからモデルを作成
    nested_dict = {"inner": {"name": "Bob", "age": 25}}
    nested_instance_from_dict = NestedModel.model_validate(nested_dict)
    print(nested_instance_from_dict)  # Output: inner=InnerModel(name='Bob', age=25)
```

ネストされたモデルを使用すると、複雑なデータ構造を型安全に扱うことができます。また、ネストされたdictからモデルを作成する際も、自動的に内部モデルのインスタンスが作成されます。

## 3.1.5 ファイル入出力

Pydanticモデルは、ファイル入出力と組み合わせることで、設定ファイルの読み書きやデータの永続化などに活用できます。

```python
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
```

このパターンは、設定ファイルやユーザーデータなどを扱う際に非常に便利です。ファイルからデータを読み込む際も、自動的にバリデーションが行われるため、安全にデータを扱うことができます。

## 3.1.6 ジェネリクス

Pydanticでは、ジェネリクスを使用して型パラメータを持つモデルを定義することができます。これは、型安全なコンテナやレスポンス型などを定義する際に便利です。

```python
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class DataContainer(BaseModel, Generic[T]):
    data: T


if __name__ == "__main__":
    # int型のデータを持つコンテナ
    int_container = DataContainer[int](data=42)
    print(int_container)  # Output: data=42

    # str型のデータを持つコンテナ
    str_container = DataContainer[str](data="Hello, World!")
    print(str_container)  # Output: data='Hello, World!'

    # 不適切なデータを渡すとエラーが発生
    invalid_container = DataContainer[int](data="Not an int")  # ValidationError
```

ジェネリクスを使用すると、同じモデル構造で異なる型のデータを扱うことができます。また、型パラメータに基づいたバリデーションも行われるため、型安全性が保証されます。

## 3.1.7 OpenAI Agents SDKでのPydanticの活用

OpenAI Agents SDKでは、Pydanticを使用してエージェントの入出力データや設定などを定義します。例えば、以下のようなユースケースがあります：

1. エージェントのレスポンス形式の定義
2. ツールの入出力パラメータの定義
3. 設定ファイルの読み込みと検証

Pydanticを使いこなすことで、型安全で堅牢なエージェントアプリケーションを開発することができます。

## まとめ

この章では、Pydanticの基本的な使い方から応用までを学びました。Pydanticを使用することで、以下のメリットが得られます：

- 型安全なデータモデルの定義
- 自動的なデータバリデーション
- JSON/dict形式との簡単な相互変換
- 複雑なデータ構造の表現
- ファイル入出力との連携
- ジェネリクスによる柔軟な型定義

次の章では、エージェント開発のもう一つの重要な要素である非同期プログラミングについて学びます。