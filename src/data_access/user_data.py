from src.config.mongoDB_client import MongodbClient
from src.constants.mongoDB_constants import USER_COLLECTION_NAME
from src.schema.user import User


class UserData:
    """
    A class for reading and writing operation of user data to mongo db

    """

    def __init__(self) -> None:
        self.client = MongodbClient()
        self.collection_name = USER_COLLECTION_NAME
        self.collection = self.client.database[self.collection_name]

    def save_user(self, user: User) -> None:
        self.collection.insert_one(user)

    def get_user(self, query: dict):
        user = self.collection.find_one(query)
        return user