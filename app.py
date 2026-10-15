```python
from flask import Flask, render_template, request
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Train the Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
model.fit(X, y)

# Flower names
flower_names = [
    name.capitalize() for name in iris.target_names
]


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    error = None
    values = ["5.1", "3.5", "1.4", "0.2"]

    if request.method == "POST":
        try:
            values = [
                request.form["sepal_length"].strip(),
                request.form["sepal_width"].strip(),
                request.form["petal_length"].strip(),
                request.form["petal_width"].strip()
            ]

            measurements = [float(value) for value in values]

            if not all(
                0 < value <= 10 for value in measurements
            ):
                raise ValueError(
                    "Measurements must be greater than 0 and at most 10."
                )

            result = model.predict([measurements])[0]
            prediction = flower_names[result]

        except (ValueError, KeyError):
            error = "Please enter four valid positive measurements (up to 10)."

    return render_template(
        "index.html",
        prediction=prediction,
        error=error,
        values=values
    )


@app.route("/health", methods=["GET"])
def health():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```
