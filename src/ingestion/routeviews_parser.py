import pandas as pd
from src.ingestion.feature_engineering import build_features

def load_routeviews(file_path: str):

    df = pd.read_csv(file_path)

    # normalize possible column names
    if "as_path" not in df.columns:
        df = df.rename(columns={
            "AS_PATH": "as_path",
            "path": "as_path"
        })

    df["prefix_length"] = df.get("prefix_length", 24)
    df["peer_asn"] = df.get("peer_asn", 0)

    return build_features(df)