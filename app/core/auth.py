from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import logging

from app.core.jwt import decode_access_token
from app.db.session import get_db
from app.models.user import User

logger = logging.getLogger(__name__)
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    try:
        logger.info(f"Received token: {credentials.credentials[:20]}...")
        payload = decode_access_token(credentials.credentials)
        logger.info(f"Decoded payload: {payload}")
        
        user_id = payload.get("sub")
        if not user_id:
            logger.error("No 'sub' in token payload")
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        # Convert string to integer for database query
        user_id = int(user_id)
        logger.info(f"Looking for user ID: {user_id}")
        
    except ValueError as e:
        logger.error(f"ValueError: {e}")
        raise HTTPException(status_code=401, detail="Invalid user ID in token")
    except Exception as e:
        logger.error(f"Token decode error: {e}")
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        logger.error(f"User not found with ID: {user_id}")
        raise HTTPException(status_code=401, detail="User not found")
    
    if not user.is_active:
        logger.error(f"User {user_id} is inactive")
        raise HTTPException(status_code=401, detail="User account is inactive")

    logger.info(f"Successfully authenticated user: {user.email}")
    return user

def get_current_admin(user: User = Depends(get_current_user)) -> User:
    logger.info(f"Checking admin role for user: {user.email}, role: {user.role}")
    if user.role.value != "admin":  # Compare with .value since it's an enum
        logger.error(f"User {user.email} has role {user.role.value}, not admin")
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
