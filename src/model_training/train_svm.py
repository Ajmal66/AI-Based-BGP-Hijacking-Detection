import pandas as pd
import joblib

from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


class SVMTrainer:

    def load_data(self):

        df = pd.read_csv(
            "datasets/processed/labeled_dataset.csv",
            low_memory=False
        )

        return df.sample(
            n=250000,
            random_state=42
        )
    
    # def load_data(self):

    #     return pd.read_csv(
    #         "datasets/processed/labeled_dataset.csv",
    #         low_memory=False
    #     )

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
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        model = Pipeline([
            (
                "scaler",
                StandardScaler()
            ),
            (
                "svm",
                SVC(
                    kernel="rbf",
                    C=1.0,
                    gamma="scale",
                )
            )
        ])

        model.fit(
            X_train,
            y_train
        )

        y_pred = model.predict(
            X_test
        )

        print("\n=== Classification Report ===")
        print(
            classification_report(
                y_test,
                y_pred
            )
        )

        print("\n=== Confusion Matrix ===")
        print(
            confusion_matrix(
                y_test,
                y_pred
            )
        )

        joblib.dump(
            model,
            "models/svm_model.pkl"
        )

        print(
            "\nModel saved to models/svm_model.pkl"
        )


def main():

    trainer = SVMTrainer()

    df = trainer.load_data()

    trainer.train(df)


if __name__ == "__main__":
    main()