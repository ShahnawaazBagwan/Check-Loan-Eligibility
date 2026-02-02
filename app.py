from flask import Flask, render_template, request
import joblib
import pandas as pd
import time

# -----------------------------
# Flask app
# -----------------------------
app = Flask(__name__)

# -----------------------------
# REQUIRED preprocessing function
# (must exist before loading model)
# -----------------------------
def binary_yes_no_mapper(X):
    return X.replace({'Yes': 1, 'No': 0})

# -----------------------------
# Load trained pipeline model
# -----------------------------
model = joblib.load("loan_approval_model.pkl")

# -----------------------------
# Feature columns (MUST match training)
# -----------------------------
FEATURE_COLUMNS = [
    'person_age',
    'person_gender',
    'person_education',
    'person_income',
    'person_emp_exp',
    'person_home_ownership',
    'loan_amnt',
    'loan_intent',
    'loan_int_rate',
    'loan_percent_income',
    'cb_person_cred_hist_length',
    'credit_score',
    'previous_loan_defaults_on_file'
]

# -----------------------------
# Home page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html", page="home")

# -----------------------------
# Prediction route
# -----------------------------
@app.route("/predict", methods=["GET", "POST"])
def predict():
    prediction = None
    probability = None
    error = None

    if request.method == "POST":
        time.sleep(1)  # loader animation delay

        try:
            # Collect form data (KEEP categorical as strings)
            input_data = {
                'person_age': int(request.form["age"]),
                'person_gender': request.form["gender"],
                'person_education': request.form["education"],
                'person_income': int(request.form["income"]),
                'person_emp_exp': int(request.form["emp_exp"]),
                'person_home_ownership': request.form["home"],
                'loan_amnt': int(request.form["loan_amnt"]),
                'loan_intent': request.form["intent"],
                'loan_int_rate': float(request.form["int_rate"]),
                'loan_percent_income': float(request.form["loan_percent_income"]),
                'cb_person_cred_hist_length': int(request.form["cred_length"]),
                'credit_score': int(request.form["credit_score"]),
                'previous_loan_defaults_on_file': request.form["previous_default"]
            }

            # Convert to DataFrame
            input_df = pd.DataFrame([input_data], columns=FEATURE_COLUMNS)

            # Prediction
            prediction = model.predict(input_df)[0]

            # Probability (only if model supports it)
            if hasattr(model.named_steps['model'], "predict_proba"):
                probability = model.predict_proba(input_df)[0][1]

        except ValueError:
            error = "Invalid input detected. Please check all fields and try again."

        except Exception:
            error = "Something went wrong. Please try again."

    return render_template(
        "index.html",
        page="predict",
        prediction=prediction,
        probability=probability,
        error=error
    )

# -----------------------------
# Run app
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)