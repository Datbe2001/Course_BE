from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)

def hash_verify_code(verify_code: str):
    return pwd_context.hash(verify_code)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

def verify_code(code: str, verify_code: str):
    return pwd_context.verify(code, verify_code)


if __name__ == '__main__':
    print(hash_password("123123"))
