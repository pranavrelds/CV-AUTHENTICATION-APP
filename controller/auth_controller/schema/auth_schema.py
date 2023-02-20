from pydantic import BaseModel

class Login(BaseModel):
    """Base model for login
    """

    email_id: str
    password: str


class Register(BaseModel):
    """
    Base model for register
    """

    name: str
    username: str
    email_id: str
    ph_no: int
    password1: str
    password2: str
