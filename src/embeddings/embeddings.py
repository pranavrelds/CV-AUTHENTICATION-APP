import io
import sys
from ast import Bytes
from typing import List

import numpy as np
from deepface import DeepFace
from deepface.commons.functions import detect_face
from PIL import Image

from src.constants.embedding_constants import (
    DETECTOR_BACKEND,
    EMBEDDING_MODEL_NAME,
    ENFORCE_DETECTION,
    SIMILARITY_THRESHOLD,
)

from src.data_access.user_embedding_data import UserEmbeddingData
from src.exception import AppException
from src.logger import logging

class UserEmbeddings:
    def __init__(self, uuid_: str) -> None:
        self.uuid_ = uuid_
        self.user_embedding_data = UserEmbeddingData()
        self.user = self.user_embedding_data.get_user_embedding(uuid_)

    def validate(self) -> bool:
        try:
            if self.user["UUID"] == None:
                return False
            if self.user["user_embed"] == None:
                return False
            return True
        except Exception as e:
            raise e

    @staticmethod
    def generate_embedding(img_array: np.ndarray) -> np.ndarray:
        """
        Generate embedding from image array"""
        try:
            faces = detect_face(
                img_array,
                detector_backend=DETECTOR_BACKEND,
                enforce_detection=ENFORCE_DETECTION,
            )
            # Generate embedding from face
            embed = DeepFace.represent(
                img_path=faces[0],
                model_name=EMBEDDING_MODEL_NAME,
                enforce_detection=False,
            )
            return embed
        except Exception as e:
            raise AppException(e, sys) from e

    @staticmethod
    def generate_embedding_list(files: List[Bytes]) -> List[np.ndarray]:
        """
        Generate embedding list from image array
        """
        embedding_list = []
        for contents in files:
            img = Image.open(io.BytesIO(contents))
            # read image array
            img_array = np.array(img)
            # Detect faces
            embed = UserEmbeddings.generate_embedding(img_array)
            embedding_list.append(embed)
        return embedding_list

    @staticmethod
    def average_embedding(embedding_list: List[np.ndarray]) -> List:
        """Method to calculate the average embedding of the list of embeddings

        Args:
            embedding_list (List[np.ndarray]): _description_

        Returns:
            List: _description_
        
        """
        avg_embed = np.mean(embedding_list, axis=0)
        return avg_embed.tolist()

    @staticmethod
    def cosine_simmilarity(db_embedding, current_embedding) -> bool:
        """Method to calculate cosine similarity between two embeddings

        Args:
            db_embedding (list): This embedding is extracted from the database
            current_embedding (list): This embedding is extracted from the current images

        Returns:
            int: simmilarity value
        """
        try:
            return np.dot(db_embedding, current_embedding) / (
                np.linalg.norm(db_embedding) * np.linalg.norm(current_embedding)
            )
        except Exception as e:
            raise AppException(e, sys) from e

    def compare_embedding(self, files: bytes) -> bool:
        """Method to compare the embedding of the current image with the embedding of the database

        Args:
            files (list): Bytes of images

        Returns:
            bool: Returns True if the similarity is greater than the threshold
        """
        try:

            if self.user:
                logging.info("Validating User Embedding ......")
                # Validate user embedding
                if self.validate() == False:
                    return False

                logging.info("Embedding Validation Successfull.......")
                # Generate embedding list

                logging.info("Generating Embedding List .......")
                embedding_list = UserEmbeddings.generate_embedding_list(
                    files
                )

                logging.info("Embedding List generated.......")
                # Calculate average embedding

                logging.info("Calculating Average Embedding .......")
                avg_embedding_list = UserEmbeddings.average_embedding(
                    embedding_list
                )
                logging.info("Average Embedding calculated.......")

                # Get embedding from database
                db_embedding = self.user["user_embed"]

                logging.info("Calculating Cosine Similarity .......")
                # Calculate cosine similarity
                simmilarity = UserEmbeddings.cosine_simmilarity(
                    db_embedding, avg_embedding_list
                )
                logging.info("Cosine Similarity calculated.......")

                if simmilarity >= SIMILARITY_THRESHOLD:
                    logging.info("User Authenticated Successfully.......")
                    return True
                else:
                    logging.info("User Authentication Failed.......")
                    return False
            logging.info("User Authentication Failed.......")

            return False
        except Exception as e:
            raise AppException(e, sys) from e
