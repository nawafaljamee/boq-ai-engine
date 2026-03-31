import pandas as pd


def find_description_column(df: pd.DataFrame):
    original_columns = list(df.columns)

    normalized_map = {
        str(col).strip().lower(): col
        for col in original_columns
    }

    exact_candidates = [
        "description",
        "desc",
        "item description",
        "work description",
        "material description",
        "scope",
        "remarks",
    ]

    for candidate in exact_candidates:
        if candidate in normalized_map:
            return normalized_map[candidate]

    partial_keywords = [
        "description",
        "desc",
        "scope",
        "remark",
        "details",
        "item",
    ]

    for col in original_columns:
        col_clean = str(col).strip().lower()
        if any(keyword in col_clean for keyword in partial_keywords):
            return col

    best_col = None
    best_score = -1

    sample_keywords = [
        "light", "lighting", "socket", "fcu",
        "oven", "pump", "charger", "panel",
        "cable", "wire", "outlet"
    ]

    for col in original_columns:
        series = df[col].dropna().astype(str).str.lower().head(20)

        if series.empty:
            continue

        score = 0

        for value in series:
            if len(value.split()) >= 2:
                score += 1

            if any(keyword in value for keyword in sample_keywords):
                score += 2

        if score > best_score:
            best_score = score
            best_col = col

    return best_col


def analyze_boq(df: pd.DataFrame) -> dict:
    description_col = find_description_column(df)

    if not description_col:
        return {
            "error": "No description column found",
            "columns": list(df.columns)
        }

    data = df[description_col].dropna().astype(str).str.lower()

    lighting = data.str.contains(r"light|lighting|led", regex=True).sum()
    sockets = data.str.contains(r"socket|outlet", regex=True).sum()
    fcu = data.str.contains(r"\bfcu\b|fan coil", regex=True).sum()
    heavy = data.str.contains(r"oven|pump|charger|heater", regex=True).sum()

    total = (lighting * 120) + (sockets * 150) + (fcu * 500) + (heavy * 700)

    return {
        "detected_description_column": description_col,
        "lighting": int(lighting),
        "sockets": int(sockets),
        "fcu": int(fcu),
        "heavy": int(heavy),
        "total_cost": int(total)
    }
