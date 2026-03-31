from io import BytesIO

from fastapi import FastAPI, UploadFile, File
import pandas as pd

from analyzer import analyze_boq

app = FastAPI()


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))
        return analyze_boq(df)

    except Exception as e:
        return {
            "error": "Failed to process file",
            "details": str(e)
        }
