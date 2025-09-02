from passlib.context import CryptContext

# Bcrypt context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

if __name__ == "__main__":
    plain_password = "Admin123!"  # Test için şifre
    hashed_password = get_password_hash(plain_password)

    print("Plain password:", plain_password)
    print("Hashed password:", hashed_password)

    # Doğrulama testleri
    print("Doğru şifre doğrulama:", verify_password("Admin123!", hashed_password))
    print("Yanlış şifre doğrulama:", verify_password("Yanlis123", hashed_password))
