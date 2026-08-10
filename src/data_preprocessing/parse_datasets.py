from src.data_preprocessing.data_loader import MRTDataLoader


def main():

    loader = MRTDataLoader()

    print("Parsing RIPE RIS...")

    ripe_dataframe = loader.parse_directory(
        "datasets/raw/ripe_ris"
    )

    loader.save_csv(
        ripe_dataframe,
        "datasets/processed/ripe_ris_parsed.csv"
    )

    print(
        f"RIPE RIS Records: {len(ripe_dataframe)}"
    )

    print("Parsing RouteViews...")

    routeviews_dataframe = loader.parse_directory(
        "datasets/raw/routeviews"
    )

    loader.save_csv(
        routeviews_dataframe,
        "datasets/processed/routeviews_parsed.csv"
    )

    print(
        f"RouteViews Records: {len(routeviews_dataframe)}"
    )

    print("Completed")


if __name__ == "__main__":
    main()