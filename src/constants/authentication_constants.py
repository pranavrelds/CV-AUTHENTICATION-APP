from src.utils.utils import CommonUtils

SECRET_KEY = CommonUtils().get_environment_variable("SECRET_KEY")
ALGORITHM = CommonUtils().get_environment_variable("ALGORITHM")