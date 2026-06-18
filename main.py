from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

app = FastAPI(
    title="Refai Portfolio API",
    description="FastAPI Backend for Ahmed Elrefai's Portfolio",
    version="1.0.0"
)

# In-memory user database placeholder (for future database/SQLAlchemy integration)
USERS_DB = []

class UserSignUp(BaseModel):
    name: str
    username: str
    password: str

class UserSignIn(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    name: str
    username: str

@app.post("/api/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignUp):
    # Check if username already exists
    if any(u["username"].lower() == user.username.lower() for u in USERS_DB):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="اسم المستخدم مسجل بالفعل." if "ar" in os.environ.get("LANG", "").lower() else "Username is already taken."
        )
    
    # Store user
    new_user = {
        "name": user.name,
        "username": user.username,
        "password": user.password  # In production, hash this password (e.g. using passlib + bcrypt)
    }
    USERS_DB.append(new_user)
    return {"name": user.name, "username": user.username}

@app.post("/api/signin", response_model=UserResponse)
async def signin(user: UserSignIn):
    # Authenticate user credentials
    matched_user = next(
        (u for u in USERS_DB if u["username"].lower() == user.username.lower() and u["password"] == user.password),
        None
    )
    if not matched_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="اسم المستخدم أو كلمة المرور غير صحيحة." if "ar" in os.environ.get("LANG", "").lower() else "Invalid username or password."
        )
    return {"name": matched_user["name"], "username": matched_user["username"]}

# ----------------------------------------------------
# SECURE ROUTING FOR STATIC FRONTEND ASSETS
# ----------------------------------------------------
@app.get("/")
async def serve_index():
    return FileResponse("index.html")

@app.get("/app.js")
async def serve_app_js():
    return FileResponse("app.js")

@app.get("/style.css")
async def serve_style_css():
    return FileResponse("style.css")

@app.get("/me.png")
async def serve_me_png():
    return FileResponse("me.png")

@app.get("/REFAI's Stats Card.png")
async def serve_stats_card_png():
    return FileResponse("REFAI's Stats Card.png")
