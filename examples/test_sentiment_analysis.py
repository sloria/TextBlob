from collections.abc import Iterable

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


def build_pipeline(
    max_features: int = 20000, ngram_range=(1, 2), stop_words="english"
) -> Pipeline:
    """Create and return a TfIDF vectorization and LinearSVC pipeline."""
    pipeline = Pipeline(
        [
            (
                "tfidf",
                TfidfVectorizer(
                    max_features=max_features,
                    ngram_range=ngram_range,
                    stop_words=stop_words,
                ),
            ),
            ("clf", LinearSVC(class_weight="balanced", random_state=42)),
        ]
    )
    return pipeline


def train_pipeline(X: Iterable[str], y: Iterable, **pipeline_kwargs) -> Pipeline:
    """Build a pipeline using "pipeline", fit it on X and y and return the trained pipeline."""
    pipeline = build_pipeline(**pipeline_kwargs)
    pipeline.fit(X, y)
    return pipeline


def predict(pipeline: Pipeline, texts: list[str]) -> list:
    """Return predictions for a list of texts using the trained pipeline or the trained model."""
    return pipeline.predict(texts)


def save_model(pipeline: Pipeline, path: str) -> None:
    """Save pipeline to local storage using joblib."""
    joblib.dump(pipeline, path)


def load_model(path: str) -> Pipeline:
    """Getting the pipeline saved with joblib."""
    return joblib.load(path)


def test_build_pipeline_returns_pipeline():
    """Testing the pipeline has the requiered fit and predict methods in it"""
    p = build_pipeline(max_features=1000)
    assert hasattr(p, "fit")
    assert hasattr(p, "predict")


def test_train_pipeline_shapes_and_predict():
    """Test for models expected lenght of output"""
    X = ["good", "bad", "average"]
    y = ["positive", "negative", "neutral"]
    p = train_pipeline(X, y, max_features=500)
    preds = predict(p, ["good", "average"])
    assert len(preds) == 2


def test_predict_types_and_values():
    """Test for the model returning correct or expected values"""
    X = ["I love this", "I hate that"]
    y = ["pos", "neg"]
    p = train_pipeline(X, y, max_features=500)
    preds = predict(p, ["I love it!"])
    # predictions should be iterable and contain strings
    assert isinstance(preds, (list, tuple)) or hasattr(preds, "__iter__")
    assert all(isinstance(x, str) for x in preds)


def test_save_load_consistency(tmp_path):
    """Test for the model being consistent after saving and loading"""
    X = ["yes", "no"]
    y = ["y", "n"]
    p = train_pipeline(X, y, max_features=300)
    out = tmp_path / "m.joblib"
    save_model(p, str(out))
    assert out.exists()
    loaded = load_model(str(out))
    preds_orig = predict(p, ["yes"])
    preds_loaded = predict(loaded, ["yes"])
    assert preds_orig.shape == preds_loaded.shape
    assert preds_orig[0] == preds_loaded[0]
