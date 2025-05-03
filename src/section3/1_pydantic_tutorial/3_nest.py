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
