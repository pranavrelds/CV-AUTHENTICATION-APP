import io
import sys

from src.data_access.user_embedding_data import UserEmbeddingData
from src.embeddings.embeddings import UserEmbeddings
from src.exception import AppException
from src.logger import logging


class UserRegisterEmbeddingValidation:
    def __init__(self, uuid_: str) -> None:
        self.uuid_ = uuid_
        self.user_embedding_data = UserEmbeddingData()

    def save_embedding(self, files: bytes):
        """Class to generate embeddings list and save it to database
        Args:
            files (dict): Bytes of images

        Returns:
            Embedding: saves the image to database
        """
        try:
            embedding_list = UserEmbeddings.generate_embedding_list(files)
            avg_embedding_list = UserEmbeddings.average_embedding(
                embedding_list
            )
            self.user_embedding_data.save_user_embedding(self.uuid_, avg_embedding_list)
        except Exception as e:
            raise AppException(e, sys) from e
