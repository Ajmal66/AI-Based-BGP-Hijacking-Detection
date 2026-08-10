import pandas as pd
from src.ingestion.feature_engineering import build_features

def load_ripe(file_path: str):

    df = pd.read_csv(file_path)

    # RIPE format normalization
    df = df.rename(columns={
        "AS_PATH": "as_path",
        "PREFIX": "prefix"
    })

    # fallback columns
    if "as_path" not in df.columns:
        raise ValueError("RIPE dataset missing AS_PATH column")

    df["prefix_length"] = df["prefix"].apply(
        lambda x: int(x.split("/")[-1]) if "/" in str(x) else 24
    )

    df["peer_asn"] = df.get("peer_asn", 0)

    return build_features(df)