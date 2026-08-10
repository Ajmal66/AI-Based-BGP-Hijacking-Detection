from pathlib import Path
from typing import List

import pandas as pd
from pybgpkit_parser import Parser

from src.data_preprocessing.logger import setup_logger


class MRTDataLoader:
    """
    Responsible for:
    - Loading MRT files
    - Parsing BGP records
    - Converting to DataFrame
    - Exporting CSV files
    """

    def __init__(self):
        self.logger = setup_logger(self.__class__.__name__)

    def get_mrt_files(self, directory: str) -> List[Path]:
        directory_path = Path(directory)

        mrt_files = []

        mrt_files.extend(directory_path.glob("*.gz"))
        mrt_files.extend(directory_path.glob("*.bz2"))

        self.logger.info(
            f"Found {len(mrt_files)} MRT files in {directory}"
        )

        return sorted(mrt_files)

    def parse_file(self, file_path: Path) -> list:

        records = []

        self.logger.info(
            f"Parsing {file_path.name}"
        )

        try:

            parser = Parser(str(file_path))

            for record in parser:

                data = record.to_dict()
                as_path = data.get("as_path")

                origin_asn = None

                if as_path:
                    path_parts = str(as_path).split()

                    if path_parts:
                        origin_asn = path_parts[-1]
                records.append({
                    "timestamp": data.get("timestamp"),
                    "peer_ip": data.get("peer_ip"),
                    "peer_asn": data.get("peer_asn"),
                    "prefix": data.get("prefix"),
                    "as_path": data.get("as_path"),
                    "origin_asn": origin_asn,
                    "next_hop": data.get("next_hop"),
                    "event_type": data.get("elem_type"),
                    "local_pref": data.get("local_pref"),
                    "med": data.get("med")
                })

        except Exception as exception:

            self.logger.error(
                f"Failed to parse {file_path.name}: {exception}"
            )

        return records
   
    def parse_directory(self, directory: str) -> pd.DataFrame:
        all_records = []

        files = self.get_mrt_files(directory)

        for file_path in files:
            records = self.parse_file(file_path)
            all_records.extend(records)

        dataframe = pd.DataFrame(all_records)

        self.logger.info(
            f"Created DataFrame with {len(dataframe)} rows"
        )

        return dataframe

    def save_csv(
        self,
        dataframe: pd.DataFrame,
        output_path: str
    ) -> None:

        output_file = Path(output_path)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        dataframe.to_csv(
            output_file,
            index=False
        )

        self.logger.info(
            f"CSV saved to {output_file}"
        )