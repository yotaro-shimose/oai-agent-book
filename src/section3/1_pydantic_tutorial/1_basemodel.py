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
