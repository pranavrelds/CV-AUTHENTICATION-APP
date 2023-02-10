import re
import sys
from typing import Optional

from passlib.context import CryptContext

from src.schema.user import User
from src.data_access.user_data import UserData
from src.constants.mongoDB_constants import USER_COLLECTION_NAME
from src.exception import AppException
from src.logger import logging

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterValidation:

    """_summary_: This class authenticates the user and returns the status
    """

    def __init__(self, user: User) -> None:
        try:
            self.user = user
            self.regex = re.compile(
                r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
            )
            self.uuid = self.user.uuid_
            self.userdata = UserData()
            self.bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        except Exception as e:
            raise e

    def validate(self) -> bool:

        """Method to check all the validation conditions for the user registration

        Returns:
            _type_: string
        """
        try:
            msg = ""
            if self.user.Name == None:
                msg += "Name is required"

            if self.user.username == None:
                msg += "Username is required"

            if self.user.email_id == None:
                msg += "Email is required"

            if self.user.ph_no == None:
                msg += "Phone Number is required"

            if self.user.password1 == None:
                msg += "Password is required"

            if self.user.password2 == None:
                msg += "Confirm Password is required"

            if not self.is_email_valid():
                msg += "Email is not valid"

            if not self.is_password_valid():
                msg += "Length of the pass`word should be between 8 and 16"

            if not self.is_password_match():
                msg += "Password does not match"

            if not self.is_details_exists():
                msg += "User already exists"

            return msg

        except Exception as e:
            raise e

    def is_email_valid(self) -> bool:
        """_summary_: Method to validates the email id

        Returns:
            bool: True if the email id is valid else False
        """
        if re.fullmatch(self.regex, self.user.email_id):
            return True
        else:
            return False

    def is_password_valid(self) -> bool:
        if len(self.user.password1) >= 8 and len(self.user.password2) <= 16:
            return True
        else:
            return False

    def is_password_match(self) -> bool:
        if self.user.password1 == self.user.password2:
            return True
        else:
            return False

    def is_details_exists(self) -> bool:
        username_val = self.userdata.get_user({"username": self.user.username})
        emailid_val = self.userdata.get_user({"email_id": self.user.email_id})
        uuid_val = self.userdata.get_user({"UUID": self.uuid})
        if username_val == None and emailid_val == None and uuid_val == None:
            return True
        return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        return bcrypt_context.hash(password)

    def validate_registration(self) -> bool:

        """Method to check all the validation conditions for the user registration
        """
        if len(self.validate()) != 0:
            return {"status": False, "msg": self.validate()}
        return {"status": True}

    def authenticate_user_registration(self) -> bool:
        """_summary_: Method to save the user details in the database
        only after validating the user details

        Returns:
            bool: _description_
        """
        try:
            logging.info("Validating the user details while Registration.....")
            if self.validate_registration()["status"]:
                logging.info("Generating the password hash.....")
                hashed_password: str = self.get_password_hash(self.user.password1)
                user_data_dict: dict = {
                    "Name": self.user.Name,
                    "username": self.user.username,
                    "password": hashed_password,
                    "email_id": self.user.email_id,
                    "ph_no": self.user.ph_no,
                    "UUID": self.uuid,
                }
                logging.info("Saving the user details in the database.....")
                self.userdata.save_user(user_data_dict)
                logging.info("Saving the user details in the database completed.....")
                return {"status": True, "msg": "User registered successfully"}
            logging.info("Validation failed while Registration.....")
            return {"status": False, "msg": self.validate()}
        except Exception as e:
            raise e
