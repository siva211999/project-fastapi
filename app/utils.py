from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_value(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_passwords):
    return pwd_context.verify(plain_password, hashed_passwords)

