from pydantic import BaseModel, ValidationError
from pydantic.networks import EmailStr
from pydantic.class_validators import validator


class AuthValidator(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def pass_validate(cls, password):
        NOT_ALLOWED_SYMBOLS = [" ", "@", "#", "'", '"', ")", "(", "%", "$", "^", "&", "*"]
        inc_sym_appears = set([
            item for item in password if item in NOT_ALLOWED_SYMBOLS
        ])
        if len(inc_sym_appears) > 0:
            raise ValueError(f"Incorrect symbols in password: {inc_sym_appears}")
        else:
            return password


if __name__ == "__main__":
    test_js = {
        "email": "asd@asd.asd",
        "password": "123wqea sd123"
    }
    try:
        a = UserEgister.parse_obj(test_js)
        print(a)
    except ValidationError as err:
        print(f"Err: {err}")