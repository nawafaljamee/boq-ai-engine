from io import BytesIO
import pandas as pd


def read_uploaded_file(contents: bytes, filename: str) -> pd.DataFrame:
    filename = filename.lower()

    if filename.endswith(".csv"):
        df = pd.read_csv(BytesIO(contents))
    elif filename.endswith((".xlsx", ".xls", ".xlsm", ".xlsb")):
        df = pd.read_excel(BytesIO(contents))
    else:
        raise ValueError("Unsupported file type")

    df.columns = df.columns.astype(str).str.strip()
    return df
