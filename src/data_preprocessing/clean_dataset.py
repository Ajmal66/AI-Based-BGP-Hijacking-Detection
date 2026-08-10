from src.data_preprocessing.data_cleaner import (
    BGPDataCleaner
)


def main():

    cleaner = BGPDataCleaner()

    print("Loading datasets...")

    ripe_df = cleaner.load_dataset(
        "datasets/processed/ripe_ris_parsed.csv"
    )

    routeviews_df = cleaner.load_dataset(
        "datasets/processed/routeviews_parsed.csv"
    )

    print("Merging datasets...")

    merged_df = cleaner.merge_datasets(
        ripe_df,
        routeviews_df
    )

    original_count = len(merged_df)

    merged_df = cleaner.remove_duplicates(
        merged_df
    )

    merged_df = cleaner.remove_missing_values(
        merged_df
    )

    merged_df = cleaner.keep_announcements_only(
        merged_df
    )

    merged_df = cleaner.remove_invalid_prefixes(
        merged_df
    )

    merged_df = cleaner.remove_invalid_as_paths(
        merged_df
    )

    final_count = len(merged_df)

    cleaner.save_dataset(
        merged_df,
        "datasets/processed/cleaned_bgp_dataset.csv"
    )

    print("\n=== Cleaning Summary ===")

    print(
        f"Original Records: {original_count:,}"
    )

    print(
        f"Final Records: {final_count:,}"
    )

    print(
        f"Removed Records: "
        f"{original_count - final_count:,}"
    )

    print(
        "\nSaved:"
    )

    print(
        "datasets/processed/cleaned_bgp_dataset.csv"
    )


if __name__ == "__main__":
    main()
