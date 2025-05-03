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
