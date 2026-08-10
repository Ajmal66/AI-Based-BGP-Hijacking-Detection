import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib


class RandomForestTrainer:

    def load_data(self):

        return pd.read_csv(
            "datasets/processed/labeled_dataset.csv",
            low_memory=False
        )

    def train(self, df):

        features = [
            "prefix_length",
            "as_path_length",
            "unique_as_count",
            "is_prepended",
            "origin_position",
            "is_origin_at_end",
            "peer_asn"
        ]

        X = df[features]
        y = df["label"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        print("\n=== Classification Report ===")
        print(classification_report(y_test, y_pred))

        print("\n=== Confusion Matrix ===")
        print(confusion_matrix(y_test, y_pred))

        joblib.dump(model, "models/random_forest.pkl")

        print("\nModel saved to models/random_forest.pkl")


def main():

    trainer = RandomForestTrainer()

    df = trainer.load_data()

    trainer.train(df)


if __name__ == "__main__":
    main()