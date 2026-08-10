from pathlib import Path
import pandas as pd
import ipaddress

from src.data_preprocessing.logger import setup_logger


class BGPDataCleaner:

    def __init__(self):
        self.logger = setup_logger(self.__class__.__name__)

    def load_dataset(self, file_path: str) -> pd.DataFrame:

        self.logger.info(
            f"Loading dataset: {file_path}"
        )

        return pd.read_csv(
            file_path,
            low_memory=False
        )

    def merge_datasets(
        self,
        ripe_df: pd.DataFrame,
        routeviews_df: pd.DataFrame
    ) -> pd.DataFrame:

        merged_df = pd.concat(
            [ripe_df, routeviews_df],
            ignore_index=True
        )

        self.logger.info(
            f"Merged dataset contains {len(merged_df)} records"
        )

        return merged_df

    def remove_duplicates(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        before_count = len(dataframe)

        dataframe = dataframe.drop_duplicates()

        removed_count = before_count - len(dataframe)

        self.logger.info(
            f"Removed {removed_count} duplicate records"
        )

        return dataframe

    def remove_missing_values(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        before_count = len(dataframe)

        dataframe = dataframe.dropna(
            subset=[
                "timestamp",
                "peer_asn",
                "prefix",
                "as_path",
                "origin_asn"
            ]
        )

        removed_count = before_count - len(dataframe)

        self.logger.info(
            f"Removed {removed_count} records with missing values"
        )

        return dataframe

    def keep_announcements_only(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        before_count = len(dataframe)

        dataframe = dataframe[
            dataframe["event_type"] == "A"
        ]

        removed_count = before_count - len(dataframe)

        self.logger.info(
            f"Removed {removed_count} non-announcement records"
        )

        return dataframe

    def validate_prefix(
        self,
        prefix: str
    ) -> bool:

        try:
            ipaddress.ip_network(
                prefix,
                strict=False
            )
            return True

        except Exception:
            return False

    def remove_invalid_prefixes(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        before_count = len(dataframe)

        dataframe = dataframe[
            dataframe["prefix"].apply(
                self.validate_prefix
            )
        ]

        removed_count = before_count - len(dataframe)

        self.logger.info(
            f"Removed {removed_count} invalid prefixes"
        )

        return dataframe

    def remove_invalid_as_paths(
        self,
        dataframe: pd.DataFrame
    ) -> pd.DataFrame:

        before_count = len(dataframe)

        dataframe = dataframe[
            dataframe["as_path"].astype(str).str.strip() != ""
        ]

        removed_count = before_count - len(dataframe)

        self.logger.info(
            f"Removed {removed_count} invalid AS paths"
        )

        return dataframe

    def save_dataset(
        self,
        dataframe: pd.DataFrame,
        output_path: str
    ):
        dataframe["origin_asn"] = (
        dataframe["origin_asn"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        )
        
        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        dataframe.to_csv(
            output_path,
            index=False
        )

        self.logger.info(
            f"Saved dataset to {output_path}"
        )