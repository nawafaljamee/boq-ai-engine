from fastapi import FastAPI, UploadFile, File
import pandas as pd

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    df = pd.read_excel(file.file)

    df.columns = df.columns.str.lower().str.strip()

    description_col = None

for col in df.columns:
    col_clean = col.lower().strip()

    if "description" in col_clean or "desc" in col_clean:
        description_col = col

   if not description_col:
    return {"error": f"Columns found: {list(df.columns)}"}

    data = df[description_col].dropna().astype(str).str.lower()

    lighting = data.str.contains("lighting").sum()
    sockets = data.str.contains("socket").sum()
    fcu = data.str.contains("fcu").sum()
    heavy = data.str.contains("oven|wh|pump|charger").sum()

    total = (lighting * 120) + (sockets * 150) + (fcu * 500) + (heavy * 700)

    return {
        "lighting": int(lighting),
        "sockets": int(sockets),
        "fcu": int(fcu),
        "heavy": int(heavy),
        "total_cost": total
    }
