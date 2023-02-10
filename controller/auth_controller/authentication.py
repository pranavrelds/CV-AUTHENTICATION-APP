import uvicorn
from fastapi import APIRouter, HTTPException, Request, Response, status
from starlette.responses import JSONResponse, RedirectResponse

from controller.auth_controller.schema.auth_schema import Login, Register
from controller.auth_controller.access_token import create_access_token

from src.schema.user import User
from src.constants.authentication_constants import ALGORITHM, SECRET_KEY
from src.validation.user_registration_validation import RegisterValidation
from src.validation.user_login_validation import LoginValidation



router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={"401": {"description": "Not Authorized!!!"}},
)


@router.post("/register", response_class=JSONResponse)
async def register_user(request: Request, register: Register):

    """Post request to register a user

    Args:
        request (Request): Request Object
        register (Register):    Name: str
                                username: str
                                email_id: str
                                ph_no: int
                                password1: str
                                password2: str

    Raises:
        e: If the user registration fails

    Returns:
        _type_: Will redirect to the embedding generation route and return the UUID of user
    """
    try:
        name = register.Name
        username = register.username
        password1 = register.password1
        password2 = register.password2
        email_id = register.email_id
        ph_no = register.ph_no

        # Add uuid to the session
        user = User(name, username, email_id, ph_no, password1, password2)
        request.session["uuid"] = user.uuid_

        # Validation of the user input data to check the format of the data
        user_registration = RegisterValidation(user)

        validate_regitration = user_registration.validate_registration()
        if not validate_regitration["status"]:
            msg = validate_regitration["msg"]
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": False, "message": msg},
            )
            return response

        # Save user if the validation is successful
        validation_status = user_registration.authenticate_user_registration()

        msg = "Registration Successful...Please Login to continue"
        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": True, "message": validation_status["msg"]},
            headers={"uuid": user.uuid_},
        )
        return response
    except Exception as e:
        raise e

    

@router.get("/register", response_class=JSONResponse)
async def authentication_page(request: Request):
    """Route for User Registration

    Returns:
        _type_: Register Response
    """
    try:
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": "Registration Page"}
        )
    except Exception as e:
        raise e


@router.post("/token")
async def login_access_token(response: Response, login):
    try:
        user_validation = LoginValidation(login.email_id, login.password)
        user: Optional[str] = user_validation.authenticate_user_login()
        if not user:
            return {"status": False, "uuid": None, "response": response}
        token_expires = timedelta(minutes=15)
        token = create_access_token(
            user["UUID"], user["username"], expires_delta=token_expires
        )
        response.set_cookie(key="access_token", value=token, httponly=True)
        return {"status": True, "uuid": user["UUID"], "response": response}
    except Exception as e:
        msg = "Failed to set access token"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": msg}
        )
        return {"status": False, "uuid": None, "response": response}


@router.post("/", response_class=JSONResponse)
async def login(request: Request, login: Login):
    """Route for User Login

    Returns:
        _type_: Login Response
    """
    try:
        msg = "Login Successful"
        response = JSONResponse(
            status_code=status.HTTP_200_OK, content={"message": msg}
        )
        token_response = await login_access_token(response=response, login=login)
        if not token_response["status"]:
            msg = "Incorrect Username and password"
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": False, "message": msg},
            )
        response.headers["uuid"] = token_response["uuid"]

        return response

    except HTTPException:
        msg = "UnKnown Error"
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"status": False, "message": msg},
        )
    except Exception as e:
        msg = "User NOT Found"
        response = JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status": False, "message": msg},
        )
        return response