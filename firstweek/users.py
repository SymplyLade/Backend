from database import db
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
import os
from dotenv import load_dotenv
import bcrypt
import uvicorn
import jwt
from middleware import create_token, verify_token
from fastapi import FastAPI, Depends, HTTPException, status


load_dotenv()

app = FastAPI(title="Simple App", version="1.0.0")

token_time = int(os.getenv("token_time"))

class Simple(BaseModel):
    name: str = Field(..., example="Samuel Larry")
    email: str = Field(..., example="sam@email.com")
    password: str = Field(..., example="sam123")
    userType: str = Field(..., example="student")
    gender: str = Field(..., example="male")

@app.post("/signup")
def signUp(input: Simple):
    try:
        # Check for duplicate email - USING 'user' TABLE
        duplicate_query = text("""
            SELECT * FROM users WHERE email = :email
        """)
        existing = db.execute(duplicate_query, {"email": input.email}).fetchone()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")
        # Insert new user - ALSO USING 'user' TABLE
        query = text("""
            INSERT INTO users (name, email, password, userType, gender)
            VALUES (:name, :email, :password, :userType, :gender)
        """)
        # Hash password
        salt = bcrypt.gensalt()
        hashedPassword = bcrypt.hashpw(input.password.encode('utf-8'), salt)
        hashed_password_str = hashedPassword.decode('utf-8')
        print(f"Hashed password: {hashed_password_str}")
        db.execute(query, {
            "name": input.name,
            "email": input.email,
            "password": hashed_password_str,
            "userType": input.userType,
            "gender": input.gender
        })
        db.commit()
        return {
            "message": "User created successfully",
            "data": {"name": input.name, "email": input.email}
            # , "password": hashedPassword, "userType": input.userType
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "Welcome to the API"}


class LoginRequest(BaseModel):
 
    email: str = Field(..., example="sam@email.com")
    password: str = Field(..., example="sam123")


@app.post("/login")
def login(input: LoginRequest):
    try:
        query = text("""
        SELECT * FROM users WHERE email = :email
""")
        result = db.execute(query, {"email": input.email}).fetchone()
        if not result:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        # Handle result as tuple or object
        hashed_password = None
        try:
            # If result is a tuple, get password by index (assuming 3rd column is password)
            if isinstance(result, tuple):
                # Adjust index if password is not at 2
                hashed_password = result[2]
            elif hasattr(result, 'password'):
                hashed_password = result.password
            else:
                raise Exception("Password field not found in result")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        verified_password = bcrypt.checkpw(input.password.encode('utf-8'), hashed_password.encode('utf-8'))

        if not verified_password:
            raise HTTPException(status_code=401, detail = "Invalid email or password")

        # Extract email and userType from the result in a robust way
        try:
            if hasattr(result, '_mapping'):
                user_email = result._mapping.get('email')
                user_type = result._mapping.get('userType')
            elif isinstance(result, dict):
                user_email = result.get('email')
                user_type = result.get('userType')
            elif hasattr(result, 'email'):
                user_email = result.email
                user_type = result.userType
            else:
                raise Exception('Unable to extract user fields from result')
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        encoded_token = create_token(details={

            "email": result.email,
            "userType": result.userType,
            "id": result.id
        }, expiry= token_time )
        return {
            "message": "Login Successful",
            "token": encoded_token,
            "expires_in_minutes": token_time
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class courseRequest(BaseModel):
    title: str = Field(..., example="Backend Course")
    level: str = Field(..., example="Beginner")

@app.post("/courses")

def addcourses(input: courseRequest, user_data = Depends (verify_token )):
    try:
        print(user_data)
        if user_data["userType"] != 'admin':
            raise HTTPException(status_code=401, detail="you are not authorized to add a course")

        query = text("""
        INSERT INTO courses(title, level)
        VALUES(:title, :level)
""")

        db.execute(query, {"title": input.title, "level": input.level})
        db.commit()

        return {
            "message": "Course added successfully",
            "data": {
                "title": input.title,
                "level": input.level
                }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class EnrollRequest(BaseModel):
    courseId: int = Field(..., example= 1)

@app.post("/enroll")
def enroll_course(input: EnrollRequest, user_data = Depends (verify_token)):
    try:
       
        if user_data["userType"] != "student":
            raise HTTPException(status_code=401, detail="Student only") 

        query = text("""
            INSERT INTO enrollments (userId, courseId)
            VALUES (:userId, :courseId)
        """)
        db.execute(query, {"userId": user_data["id"], "courseId": input.courseId})
        db.commit()

        return {
            "message": "Enrollment successful",
            "data": {
                "userId": user_data["id"],
                "courseId": input.courseId
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))





if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("host"), port=int(os.getenv("port")))

