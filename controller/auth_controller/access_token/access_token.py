from typing import Optional
from datetime import datetime, timedelta

from jose import JWTError, jwt

from src.constants.authentication_constants import ALGORITHM, SECRET_KEY

def create_access_token(
    uuid: str, username: str, expires_delta: Optional[timedelta] = None
) -> str:
    """Function to create the access token

    Args:
        uuid (str): uuid of the user
        username (str): username of the user

    Raises:
        e: _description_

    Returns:
        _type_: _description_
    """

    try:
        secret_key = SECRET_KEY
        algorithm = ALGORITHM

        encode = {"sub": uuid, "username": username}
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        encode.update({"exp": expire})
        return jwt.encode(encode, secret_key, algorithm=algorithm)
    except Exception as e:
        raise e