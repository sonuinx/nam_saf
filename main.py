import os
from typing import Dict

import pandas as pd
from database import SessionLocal
from excel_controller import append_record_to_excel
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from models import UserDB
from passlib.context import CryptContext
from schema import User
from fastapi.middleware.cors import CORSMiddleware
import json
base_path = os.path.dirname(__file__)
app = FastAPI()
allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db_users = []


@app.get("/assets/")
async def read_assets_data():
    try:
        # Read data from Excel file
        with pd.ExcelFile(f"{base_path}/excel_files/Assets_A.xlsx") as xls:
            df = pd.read_excel(xls, sheet_name="steel")

            df_cleaned = df.where(pd.notna(df), None)
            df_cleaned["year"] = df_cleaned["year"].astype("Int64")
            # Convert DataFrame to a list of dictionaries
            sheet_data = df_cleaned.to_dict(orient="records")
            
            # Replace spaces with underscores in keys
            for item in sheet_data:
                for key in list(item.keys()):
                    if ' ' in key:
                        new_key = key.replace(' ', '_')
                        item[new_key] = item.pop(key)
            # Replace None or NaN values with None
            for item in sheet_data:
                for k, v in item.items():
                    if v is None or pd.isna(v):
                        item[k] = None
            response_data = {"data": sheet_data}

        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/assets/")
async def insert_assets(record: Dict):
    try:
        append_record_to_excel(record, file_name="Assets_A.xlsx", sheet_name="steel")
        return {"message": "Record inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/projects/")
async def insert_projects(record: Dict):
    try:
        append_record_to_excel(record, file_name="Project.xlsx", sheet_name="project")
        return {"message": "Record inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/projects/")
async def read_projects_data():
    try:
        # Read data from Excel file
        with pd.ExcelFile(f"{base_path}/excel_files/Project.xlsx") as xls:
            df = pd.read_excel(xls, sheet_name="project")

            df_cleaned = df.where(pd.notna(df), None)
            # Convert DataFrame to a list of dictionaries
            sheet_data = df_cleaned.to_dict(orient="records")
            # Replace spaces with underscores in keys
            for item in sheet_data:
                for key in list(item.keys()):
                    if ' ' in key:
                        new_key = key.replace(' ', '_')
                        item[new_key] = item.pop(key)


            response_data = {"data": sheet_data}
        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/portfolio/")
async def read_portfolio_data():
    try:
        # Read data from Excel file
        with pd.ExcelFile(f"{base_path}/excel_files/Portfolio.xlsx") as xls:
            df = pd.read_excel(xls, sheet_name="Creating portfolio")

            df_cleaned = df.where(pd.notna(df), None)
            # Convert DataFrame to a list of dictionaries
            sheet_data = df_cleaned.to_dict(orient="records")
            # Replace spaces with underscores in keys
            for item in sheet_data:
                for key in list(item.keys()):
                    if ' ' in key:
                        new_key = key.replace(' ', '_')
                        item[new_key] = item.pop(key)


            response_data = {"data": sheet_data}
        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/portfolio/")
async def insert_portfolio(record: Dict):
    try:
        append_record_to_excel(
            record, file_name="Portfolio.xlsx", sheet_name="Creating portfolio"
        )
        return {"message": "Record inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# User registration
def register_user(user: User):
    hashed_password = get_password_hash(user.hashed_password)
    db_user = UserDB(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db = SessionLocal()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user


# User login
def authenticate_user(username: str, password: str):
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db.close()
    return user


# User registration endpoint
@app.post("/register/")
def register(user: User):
    db_user = register_user(user)
    return {"message": "User registered successfully", "user_id": db_user.id}


# User login endpoint
@app.post("/login/")
def login(username: str, password: str):
    user = authenticate_user(username, password)
    return {"message": "Login successful", "user_id": user.id}
