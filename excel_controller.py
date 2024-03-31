import os
from typing import Dict

import pandas as pd
from fastapi import HTTPException

base_path = os.path.dirname(__file__)
# Function to append record to Excel sheet
def append_record_to_excel(record: Dict,file_name=None,sheet_name=None):
    try:
        # Read existing data from Excel file
        df = pd.read_excel(f'{base_path}/excel_files/{file_name}', sheet_name=sheet_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Convert NaN values to None
    record = {key: value if pd.notna(value) else None for key, value in record.items()}
    
    # Convert record to DataFrame
    new_df = pd.DataFrame([record])

    # Concatenate existing DataFrame with new record
    df = pd.concat([df, new_df], ignore_index=True)
    
    # Write DataFrame back to Excel file
    df.to_excel(f'{base_path}/excel_files/{file_name}', sheet_name=sheet_name, index=False)