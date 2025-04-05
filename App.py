from flask import Flask, render_template, request

app = Flask(__name__)

# Expanded knowledge base with symptoms & risk factors
knowledge_base = {
    "cervical cancer": [
        "abnormal vaginal bleeding",
        "pelvic pain",
        "pain during intercourse",
        "unusual vaginal discharge",
        "lower back pain",
        "fatigue",
        "weight loss",
        "swelling in legs"
    ]
}

# Risk Factors
risk_factors = {
    "age_group": {"40+": "Higher risk", "below 40": "Lower risk"},
    "vaccination": {"no": "Higher risk", "yes": "Lower risk"},
    "partners": {"yes": "Higher risk", "no": "Lower risk"},
    "family_history": {"no": "Higher risk", "yes": "Lower risk"}
}

# Diagnosis function
def diagnose(symptoms, risk_answers):
    matches = {}
    for condition, condition_symptoms in knowledge_base.items():
        match_count = sum(1 for symptom in symptoms if symptom.lower() in condition_symptoms)
        if match_count > 0:
            matches[condition] = match_count

    risk_summary = [risk_factors[key][value] for key, value in risk_answers.items() if value in risk_factors[key]]
    risk_level = " & ".join(risk_summary)

    if matches:
        best_match = max(matches, key=matches.get)
        return f"⚠️ You might have {best_match}. Risk Factors: {risk_level}. Please consult a doctor."
    else:
        return f"✅ No strong match found for cervical cancer. Risk Factors: {risk_level}. Please visit a doctor if concerned."

@app.route("/", methods=["GET", "POST"])
def home():
    diagnosis = None
    if request.method == "POST":
        symptoms = request.form.getlist("symptoms")
        risk_answers = {
            "age_group": request.form.get("age_group"),
            "vaccination": request.form.get("vaccination"),
            "partners": request.form.get("partners"),
            "family_history": request.form.get("family_history")
        }
        diagnosis = diagnose(symptoms, risk_answers)

    return render_template("index.html", diagnosis=diagnosis, knowledge_base=knowledge_base)

if __name__ == "__main__":
    app.run(debug=True)
