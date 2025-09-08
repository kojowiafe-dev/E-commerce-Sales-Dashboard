from passlib.context import CryptContext

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pass_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pass_context.verify(plain_password, hashed_password)