import os
import shutil

from src.data_preprocessing.data_loader import MRTDataLoader
from src.data_preprocessing.data_cleaner import BGPDataCleaner

from src.ingestion.csv_loader import load_csv
from src.ingestion.ripe_parser import load_ripe
from src.ingestion.routeviews_parser import load_routeviews

RAW_UPLOAD_DIR = "uploads/raw"
PROCESSED_UPLOAD_DIR = "uploads/processed"


def clear_directory(directory: str):
    """
    Remove all files from a directory.
    """

    os.makedirs(directory, exist_ok=True)

    for file in os.listdir(directory):
        path = os.path.join(directory, file)

        if os.path.isfile(path):
            os.remove(path)


def load_any_file(file_path: str, dataset_type: str, limit: int = None):

    # ----------------------------------------------------
    # CUSTOM FEATURE-ENGINEERED CSV
    # ----------------------------------------------------

    if dataset_type == "csv":

        df = load_csv(file_path)

        if limit is not None:
            df = df.head(limit)

        return df

    # ----------------------------------------------------
    # RAW MRT FILES
    # ----------------------------------------------------

    ext = os.path.splitext(file_path)[1].lower()

    if dataset_type == "ripe":

        if ext not in [".gz", ".csv"]:
            raise ValueError("RIPE RIS supports .gz or processed .csv files only.")

    elif dataset_type == "routeviews":

        if ext not in [".bz2", ".csv"]:
            raise ValueError("RouteViews supports .bz2 or processed .csv files only.")


    # ----------------------------------------------------
    # PREPARE UPLOAD DIRECTORIES
    # ----------------------------------------------------

    clear_directory(RAW_UPLOAD_DIR)
    clear_directory(PROCESSED_UPLOAD_DIR)

    destination = os.path.join(RAW_UPLOAD_DIR, os.path.basename(file_path))

    shutil.copy2(file_path, destination)

    # ----------------------------------------------------
    # PARSE MRT FILE
    # ----------------------------------------------------

    loader = MRTDataLoader()

    parsed_df = loader.parse_directory(RAW_UPLOAD_DIR)

    if limit is not None:
        parsed_df = parsed_df.head(limit)

    parsed_csv = os.path.join(PROCESSED_UPLOAD_DIR, "uploaded_parsed.csv")

    loader.save_csv(parsed_df, parsed_csv)

    # ----------------------------------------------------
    # CLEAN DATA
    # ----------------------------------------------------

    cleaner = BGPDataCleaner()

    cleaned_df = cleaner.load_dataset(parsed_csv)

    cleaned_df = cleaner.remove_duplicates(cleaned_df)

    cleaned_df = cleaner.remove_missing_values(cleaned_df)

    cleaned_df = cleaner.keep_announcements_only(cleaned_df)

    cleaned_df = cleaner.remove_invalid_prefixes(cleaned_df)

    cleaned_df = cleaner.remove_invalid_as_paths(cleaned_df)

    cleaned_csv = os.path.join(PROCESSED_UPLOAD_DIR, "uploaded_cleaned.csv")

    cleaner.save_dataset(cleaned_df, cleaned_csv)

    # ----------------------------------------------------
    # FEATURE EXTRACTION
    # ----------------------------------------------------

    if dataset_type == "ripe":
        return load_ripe(cleaned_csv)

    return load_routeviews(cleaned_csv)
