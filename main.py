from fastapi import FastAPI, UploadFile, File
import pandas as pd

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        # قراءة الملف
        df = pd.read_excel(file.file)

        # تنظيف أسماء الأعمدة
        df.columns = df.columns.astype(str).str.lower().str.strip()

        # البحث عن عمود الوصف
        description_col = None
        for col in df.columns:
            if "description" in col or "desc" in col:
                description_col = col
                break

        # إذا ما حصل العمود
        if not description_col:
            return {
                "error": "No description column found",
                "columns": list(df.columns)
            }

        # تنظيف البيانات
        data = df[description_col].dropna().astype(str).str.lower()

        # تحليل البيانات
        lighting = data.str.contains("lighting").sum()
        sockets = data.str.contains("socket").sum()
        fcu = data.str.contains("fcu").sum()
        heavy = data.str.contains("oven|wh|pump|charger").sum()

        # حساب التكلفة
        total = (lighting * 120) + (sockets * 150) + (fcu * 500) + (heavy * 700)

        return {
            "lighting": int(lighting),
            "sockets": int(sockets),
            "fcu": int(fcu),
            "heavy": int(heavy),
            "total_cost": int(total)
        }

    except Exception as e:
        return {
            "error": "Failed to process file",
            "details": str(e)
        }
