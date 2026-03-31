from io import BytesIO

from fastapi import FastAPI, UploadFile, File
import pandas as pd

from analyzer import analyze_boq

app = FastAPI()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        filename = file.filename.lower()

        if filename.endswith(".csv"):
            df = pd.read_csv(BytesIO(contents))
        elif filename.endswith((".xlsx", ".xls", ".xlsm", ".xlsb")):
            df = pd.read_excel(BytesIO(contents))
        else:
            return {"error": "Unsupported file type"}

        df.columns = df.columns.astype(str).str.strip()
        return analyze_boq(df)

    except Exception as e:
        return {
            "error": "Failed to process file",
            "details": str(e)
        }
