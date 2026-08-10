import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Embedding
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


class LSTMTrainer:

    def load_data(self):
        df = pd.read_csv(
            "datasets/processed/labeled_dataset.csv",
            low_memory=False
        )

        return df.sample(n=100000, random_state=42)

    def train(self, df):

        # -----------------------------
        # STEP 1: AS PATH
        # -----------------------------
        df["as_path"] = df["as_path"].astype(str)
        paths = df["as_path"].tolist()

        # -----------------------------
        # STEP 2: TOKENIZATION
        # -----------------------------
        tokenizer = Tokenizer(
            filters="",
            lower=False,
            split=" "
        )

        tokenizer.fit_on_texts(paths)

        sequences = tokenizer.texts_to_sequences(paths)

        MAX_LEN = 64

        # -----------------------------
        # SAVE TOKENIZER + MAX_LEN
        # -----------------------------
        joblib.dump(tokenizer, "models/lstm_tokenizer.pkl")
        joblib.dump(MAX_LEN, "models/lstm_maxlen.pkl")

        # -----------------------------
        # STEP 3: PADDING
        # -----------------------------
        X = pad_sequences(
            sequences,
            maxlen=MAX_LEN,
            padding="post"
        )

        # -----------------------------
        # STEP 4: LABELS
        # -----------------------------
        y = df["label"].values

        # -----------------------------
        # STEP 5: TRAIN TEST SPLIT
        # -----------------------------
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        vocab_size = len(tokenizer.word_index) + 1

        # -----------------------------
        # STEP 6: LSTM MODEL (FIXED)
        # -----------------------------
        model = Sequential()

        # 🔥 Embedding layer (IMPORTANT FIX)
        model.add(
            Embedding(
                input_dim=vocab_size,
                output_dim=64,
                input_length=MAX_LEN
            )
        )

        model.add(
            LSTM(64)
        )

        model.add(
            Dropout(0.2)
        )

        model.add(
            Dense(32, activation="relu")
        )

        model.add(
            Dense(1, activation="sigmoid")
        )

        model.compile(
            optimizer="adam",
            loss="binary_crossentropy",
            metrics=["accuracy"]
        )

        # -----------------------------
        # STEP 7: TRAIN
        # -----------------------------
        model.fit(
            X_train,
            y_train,
            epochs=20,
            batch_size=64,
            validation_split=0.1,
            verbose=1
        )

        # -----------------------------
        # STEP 8: EVALUATION
        # -----------------------------
        y_pred = model.predict(X_test)
        y_pred = (y_pred > 0.5).astype(int).flatten()

        print("\n=== Classification Report ===")
        print(classification_report(y_test, y_pred))

        print("\n=== Confusion Matrix ===")
        print(confusion_matrix(y_test, y_pred))

        # -----------------------------
        # STEP 9: SAVE MODEL
        # -----------------------------
        model.save("models/lstm_model.keras")

        print("\nModel saved to models/lstm_model.keras")


def main():
    trainer = LSTMTrainer()
    df = trainer.load_data()
    trainer.train(df)


if __name__ == "__main__":
    main()