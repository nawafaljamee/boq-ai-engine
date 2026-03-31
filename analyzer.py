import pandas as pd


def find_description_column(df: pd.DataFrame):
    df.columns = df.columns.astype(str).str.lower().str.strip()

    for col in df.columns:
        if "description" in col or "desc" in col:
            return col

    return None


def analyze_boq(df: pd.DataFrame) -> dict:
    description_col = find_description_column(df)

    if not description_col:
        return {
            "error": "No description column found",
            "columns": list(df.columns)
        }

    data = df[description_col].dropna().astype(str).str.lower()

    lighting = data.str.contains(r"lighting", regex=True).sum()
    sockets = data.str.contains(r"socket", regex=True).sum()
    fcu = data.str.contains(r"fcu", regex=True).sum()
    heavy = data.str.contains(r"oven|pump|charger", regex=True).sum()

    total = (lighting * 120) + (sockets * 150) + (fcu * 500) + (heavy * 700)

    return {
        "lighting": int(lighting),
        "sockets": int(sockets),
        "fcu": int(fcu),
        "heavy": int(heavy),
        "total_cost": int(total)
    }
