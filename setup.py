from setuptools import find_packages, setup

# Declaring variables for setup functions
PROJECT_NAME = "CV-FACE-AUTHENTICATOR"
VERSION = "0.0.1"
AUTHOR = "Pranav Tondgaonkar"
DESRCIPTION = "A two-stage face authentication system using MTCNN and FaceNet"


setup(
    name=PROJECT_NAME,
    version=VERSION,
    author=AUTHOR,
    description=DESRCIPTION,
    packages=find_packages(),
)
