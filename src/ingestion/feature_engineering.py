import pandas as pd

def build_features(df: pd.DataFrame):

    df = df.copy()

    # ensure string AS_PATH
    df["as_path"] = df["as_path"].astype(str)

    # feature 1
    df["as_path_length"] = df["as_path"].apply(lambda x: len(x.split()))

    # feature 2
    df["unique_as_count"] = df["as_path"].apply(lambda x: len(set(x.split())))

    # feature 3
    df["origin_position"] = df["as_path"].apply(lambda x: len(x.split()) - 1)

    # feature 4
    df["is_origin_at_end"] = 1  # simplified assumption

    # feature 5 (placeholder if not available)
    if "is_prepended" not in df.columns:
        df["is_prepended"] = df["as_path"].apply(lambda x: 1 if "99999 99999" in x else 0)

    return df