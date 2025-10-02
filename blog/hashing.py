import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    @staticmethod
    def bcrypt(password: str):
        # Pre-hash to avoid 72-byte limit
        sha256 = hashlib.sha256(password.encode("utf-8")).hexdigest()
        return pwd_context.hash(sha256)

    @staticmethod
    def verify(hashed_password, plain_password):
        sha256 = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
        return pwd_context.verify(sha256, hashed_password)
