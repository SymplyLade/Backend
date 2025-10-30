import jwt
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Security, HTTPException, status

# Initialize bearer authentication
bearer = HTTPBearer()

# Load environment variables
load_dotenv()

secret_key = os.getenv("SECRET_KEY")

if not secret_key:
    raise RuntimeError("SECRET_KEY not set in environment (.env) - cannot create tokens")

# Function to create JWT
def create_token(details: dict, expiry: int = 30):
    expire = datetime.utcnow() + timedelta(minutes=expiry)
    details.update({"exp": expire})
    token = jwt.encode(details, secret_key, algorithm="HS256")
    return token


#  Function to verify JWT
def verify_token(credentials: HTTPAuthorizationCredentials = Security(bearer)):
    token = credentials.credentials  #  Extract the actual token string

    try:
        verified_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        return {
            "email": verified_token.get("email"),
            "userType": verified_token.get("userType"),
            "id": verified_token.get("id"),
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
