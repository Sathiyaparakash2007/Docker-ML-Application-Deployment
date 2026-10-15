from flask import Flask, request, jsonify, render_template
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Load dataset
iris = load_iris()

# Train the ML model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(iris.data, iris.target)


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    error = None

    if request.method == "POST":
        try:
            features = [
                float(request.form["sepal_length"]),
                float(request.form["sepal_width"]),
                float(request.form["petal_length"]),
                float(request.form["petal_width"])
            ]

            if not all(0 <= value <= 10 for value in features):
                raise ValueError

            result = model.predict([features])[0]
            prediction = iris.target_names[result].title()

        except (ValueError, KeyError):
            error = "Please enter valid measurements between 0 and 10."

    return render_template(
        "index.html",
        prediction=prediction,
        error=error
    )


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        features = [float(value) for value in data["features"]]

        if len(features) != 4:
            return jsonify({"error": "Exactly four features are required"}), 400

        if not all(0 <= value <= 10 for value in features):
            return jsonify({"error": "Measurements must be between 0 and 10"}), 400

        result = model.predict([features])[0]

        return jsonify({
            "prediction": iris.target_names[result],
            "model": "RandomForestClassifier"
        })

    except (ValueError, KeyError, TypeError):
        return jsonify({"error": "Invalid input"}), 400


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
