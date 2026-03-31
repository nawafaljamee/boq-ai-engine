from fastapi import FastAPI, UploadFile, File

from analyzer import analyze_boq
from reader import read_uploaded_file

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "BOQ AI Engine is running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = read_uploaded_file(contents, file.filename)
        return analyze_boq(df)

    except Exception as e:
        return {
            "error": "Failed to process file",
            "details": str(e)
        }
