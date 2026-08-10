import pandas as pd


class BGPFeatureExtractor:

    def __init__(self):
        pass

    def extract_prefix_length(self, prefix: str) -> int:
        try:
            return int(prefix.split("/")[-1])
        except:
            return 0

    def as_path_features(self, as_path: str):

        if not isinstance(as_path, str):
            return 0, 0, 0

        asns = as_path.strip().split()

        path_length = len(asns)
        unique_count = len(set(asns))
        is_prepended = int(path_length != unique_count)

        return path_length, unique_count, is_prepended

    def origin_position(self, as_path: str, origin_asn: str):

        try:
            asns = as_path.split()
            return asns.index(str(origin_asn))
        except:
            return -1

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:

        df["prefix_length"] = df["prefix"].apply(self.extract_prefix_length)

        df["as_path_length"] = df["as_path"].apply(
            lambda x: self.as_path_features(x)[0]
        )

        df["unique_as_count"] = df["as_path"].apply(
            lambda x: self.as_path_features(x)[1]
        )

        df["is_prepended"] = df["as_path"].apply(
            lambda x: self.as_path_features(x)[2]
        )

        df["origin_position"] = df.apply(
            lambda row: self.origin_position(
                row["as_path"],
                row["origin_asn"]
            ),
            axis=1
        )

        df["is_origin_at_end"] = (
            df["origin_position"] == (df["as_path_length"] - 1)
        ).astype(int)

        return df