import pandas as pd
import json
import io


def format_parameters_table(results: list) -> pd.DataFrame:
    """
    Converts list of parameter-value dicts into a DataFrame.
    """
    if not results:
        return pd.DataFrame(columns=["parameter", "value"])

    return pd.DataFrame(results)


def export_csv(df: pd.DataFrame) -> bytes:
    """
    Return CSV as bytes for Streamlit download button
    """
    return df.to_csv(index=False).encode("utf-8")


def export_json(df: pd.DataFrame) -> str:
    """
    Return JSON string for Streamlit text display or download
    """
    return df.to_json(orient="records", indent=2)