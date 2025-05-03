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
