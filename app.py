from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import pandas as pd
from src.prediction.detector import run_detection
import zipfile
import bz2
import gzip
from src.prediction_pipeline.upload_pipeline import UploadPipeline


pipeline = UploadPipeline()
app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
SAMPLE_FOLDER = "datasets/sample"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
os.makedirs(SAMPLE_FOLDER, exist_ok=True)
REQUIRED_CSV_COLUMNS = [
    "prefix_length",
    "as_path_length",
    "unique_as_count",
    "is_prepended",
    "origin_position",
    "is_origin_at_end",
    "peer_asn",
    "as_path"
]

ALLOWED_EXT = {".csv"}

@app.route("/")
def dashboard():

    try:
        # df = pd.read_csv("datasets/processed/labeled_dataset.csv")

        # total_routes = len(df)
        # hijacks = int((df["label"] == 1).sum())
        # normal = int((df["label"] == 0).sum())
        total_routes = 1400977
        hijacks = 30000
        normal = 1370977

        detection_rate = round((hijacks / total_routes) * 100, 2)

    except Exception:
        total_routes = 0
        hijacks = 0
        normal = 0
        detection_rate = 0

    return render_template(
        "dashboard.html",
        total=total_routes,
        hijacks=hijacks,
        normal=normal,
        rate=detection_rate
    )


@app.route("/upload")
def upload_page():
    return render_template("upload.html")


@app.route("/results")
def results_page():
    return render_template("results.html")


# @app.route("/upload-file", methods=["POST"])
# def upload_file():
#     file = request.files["file"]
#     model_type = request.form.get("model")
#     dataset_type = request.form.get("dataset_type")

#     file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#     file.save(file_path)

#     output_path = os.path.join(RESULT_FOLDER, "predictions.csv")

#     result = run_detection(file_path, model_type, output_path)

#     return jsonify(result)

# -------------------------
# Helpers
# -------------------------

# -------------------------
# Helpers
# -------------------------

def is_zip(file_path):
    return zipfile.is_zipfile(file_path)


def read_csv_safe(file_obj):
    """
    Safe CSV reader for messy BGP datasets
    """

    try:
        return pd.read_csv(file_obj)
    except Exception:
        # fallback for dirty RouteViews format
        return pd.read_csv(
            file_obj,
            sep=None,              # auto-detect delimiter
            engine="python",      # more flexible parser
            on_bad_lines="skip"   # skip broken lines
        )


def load_compressed_csv(file_path):

    ext = os.path.splitext(file_path)[1].lower()

    # -------------------------
    # ZIP FILE
    # -------------------------
    if ext == ".zip":
        with zipfile.ZipFile(file_path, "r") as z:

            csv_files = [
                f for f in z.namelist()
                if f.endswith(".csv") or f.endswith(".txt")
            ]

            if not csv_files:
                raise ValueError("ZIP file does not contain readable dataset")

            with z.open(csv_files[0]) as f:
                return read_csv_safe(f)

    # -------------------------
    # BZ2 FILE (RouteViews)
    # -------------------------
    if ext == ".bz2":
        with bz2.open(file_path, "rt", encoding="utf-8", errors="ignore") as f:
            return read_csv_safe(f)

    # -------------------------
    # GZ FILE (RIPE common format)
    # -------------------------
    if ext == ".gz":
        with gzip.open(file_path, "rt", encoding="utf-8", errors="ignore") as f:
            return read_csv_safe(f)

    # -------------------------
    # NORMAL CSV
    # -------------------------
    return read_csv_safe(file_path)

# def process_uploaded_raw(file_path):
#     """
#     Run full pipeline ONLY on uploaded dataset
#     """

#     # Step 1: Load raw file
#     raw_df = load_compressed_csv(file_path)

#     # Step 2: Parse
#     from src.data_preprocessing.parse_datasets import Parser
#     parser = Parser()
#     parsed_df = parser.run(raw_df)

#     # Step 3: Clean
#     from src.data_preprocessing.clean_dataset import Cleaner
#     cleaner = Cleaner()
#     cleaned_df = cleaner.run(parsed_df)

#     # Step 4: Feature engineering
#     from src.feature_engineering.build_features import FeatureBuilder
#     builder = FeatureBuilder()
#     feature_df = builder.run(cleaned_df)

#     return feature_df

# -------------------------
# ROUTE
# -------------------------

@app.route("/upload-file", methods=["POST"])
def upload_file():

    try:

        file = request.files.get("file")
        model_type = request.form.get("model")
        dataset_type = request.form.get("dataset_type")
        limit = request.form.get("limit", "").strip()

        if limit:
            try:
                limit = int(limit)

                if limit <= 0:
                    raise ValueError()

            except ValueError:
                return jsonify({
                    "error": "Record limit must be a positive integer."
                }), 400

        else:
            limit = None
        # --------------------------------------------------
        # BASIC VALIDATION
        # --------------------------------------------------

        if not file or file.filename == "":
            return jsonify({
                "error": "Please select a file to upload."
            }), 400

        if dataset_type not in ["csv", "ripe", "routeviews"]:
            return jsonify({
                "error": "Invalid dataset type selected."
            }), 400

        ext = os.path.splitext(file.filename)[1].lower()

        # --------------------------------------------------
        # FILE TYPE VALIDATION
        # --------------------------------------------------

        if dataset_type == "csv":

            if ext != ".csv":
                return jsonify({
                    "error": "Custom CSV mode accepts only .csv files."
                }), 400

        elif dataset_type == "ripe":

            if ext not in [".gz"]:
                return jsonify({
                    "error": "RIPE RIS supports .gz (raw MRT) files only."
                }), 400

        elif dataset_type == "routeviews":

            if ext not in [".bz2"]:
                return jsonify({
                    "error": "RouteViews supports .bz2 (raw MRT) files only."
                }), 400

        # --------------------------------------------------
        # SAVE FILE
        # --------------------------------------------------

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(file_path)

        # --------------------------------------------------
        # RUN PREPROCESSING PIPELINE
        # --------------------------------------------------

        df = pipeline.run(
            file_path,
            dataset_type,
            limit
        )

        # --------------------------------------------------
        # VERIFY REQUIRED FEATURES
        # --------------------------------------------------

        required_features = [
            "prefix_length",
            "as_path_length",
            "unique_as_count",
            "is_prepended",
            "origin_position",
            "is_origin_at_end",
            "peer_asn"
        ]

        missing = [
            col for col in required_features
            if col not in df.columns
        ]

        if missing:
            return jsonify({
                "error": f"Feature extraction failed. Missing columns: {', '.join(missing)}"
            }), 400

        # --------------------------------------------------
        # RUN MODEL
        # --------------------------------------------------

        output_path = os.path.join(
            RESULT_FOLDER,
            "predictions.csv"
        )

        result = run_detection(
            df,
            model_type,
            output_path
        )

        return jsonify(result)

    except ValueError as e:

        return jsonify({
            "error": str(e)
        }), 400

    except Exception as e:

        return jsonify({
            "error": f"Processing failed: {str(e)}"
        }), 500


@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory("results", filename, as_attachment=True)

@app.route("/sample-csv")
def sample_csv():

    return send_from_directory(
        SAMPLE_FOLDER,
        "sample_bgp_dataset.csv",
        as_attachment=True
    )

@app.route("/guide")
def guide():
    return render_template("guide.html")

if __name__ == "__main__":
    app.run(debug=True)