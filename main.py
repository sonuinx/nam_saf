import os
from typing import Dict

import pandas as pd
from excel_controller import append_record_to_excel
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

base_path = os.path.dirname(__file__)
app = FastAPI()


@app.get("/assets/")
async def read_assets_data():
    try:
        # Read data from Excel file
        with pd.ExcelFile(f'{base_path}/excel_files/Assets_A.xlsx') as xls:

            df = pd.read_excel(xls, sheet_name="steel")

            df_cleaned = df.where(pd.notna(df), None)
            df_cleaned['year'] = df_cleaned['year'].astype('Int64')
            # Convert DataFrame to a list of dictionaries
            sheet_data = df_cleaned.to_dict(orient='records')

            response_data = {"data": sheet_data}
        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/assets/")
async def insert_assets(record: Dict):
    try:
        append_record_to_excel(record,file_name="Assets_A.xlsx",sheet_name="steel")
        return {"message": "Record inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/projects/")
async def insert_projects(record: Dict):
    try:
        append_record_to_excel(record,file_name="Project.xlsx",sheet_name="project")
        return {"message": "Record inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/projects/")
async def read_projects_data():
    try:
        # Read data from Excel file
        with pd.ExcelFile(f'{base_path}/excel_files/Project.xlsx') as xls:

            df = pd.read_excel(xls, sheet_name="project")

            df_cleaned = df.where(pd.notna(df), None)
            # Convert DataFrame to a list of dictionaries
            sheet_data = df_cleaned.to_dict(orient='records')

            response_data = {"data": sheet_data}
        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/portfolio/")
async def read_portfolio_data():
    try:
        # Read data from Excel file
        with pd.ExcelFile(f'{base_path}/excel_files/Portfolio.xlsx') as xls:

            df = pd.read_excel(xls, sheet_name="Creating portfolio")

            df_cleaned = df.where(pd.notna(df), None)
            # Convert DataFrame to a list of dictionaries
            sheet_data = df_cleaned.to_dict(orient='records')

            response_data = {"data": sheet_data}
        return JSONResponse(content=response_data, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/portfolio/")
async def insert_portfolio(record: Dict):
    try:
        append_record_to_excel(record,file_name="Portfolio.xlsx",sheet_name="Creating portfolio")
        return {"message": "Record inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))