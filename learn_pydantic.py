from datetime import datetime
from pydantic import BaseModel, ConfigDict, ValidationError


class User(BaseModel):
    id: int
    name: str = 'Jane Doe'
    signup_ts: str | None = None # Optional field

    model_config = ConfigDict(extra='allow', str_max_length=20) # 限制字符串最大长度为20

class Number(BaseModel):
    a: int
    b: float
    c: str


def main():
    # Pydantic may cast input data to force it to conform to model field types
    number = Number(a=1, b='2.5', c="Hello, Pydantic!")
    print(number)
    print(number.model_dump()) # 以字典形式输出
    print(number.a)  # 访问字段

    try:
        m = User.model_validate_json('{"id": 123, "name": 123}')
    except ValidationError as e:
     print(e)


if __name__ == "__main__":
    main()
