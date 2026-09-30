from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import sqlite3
from recommend import recommend_roles, get_skill_gap

app = Flask(__name__)
CORS(app)

model = joblib.load("model/placement_model.pkl")

@app.route("/")
def home():
    return "Flask server chal raha hai! Model bhi load ho gaya."


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    conn = sqlite3.connect("backend/placement_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id, name FROM users WHERE email = ?", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        user_id = existing_user[0]
    else:
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
        conn.commit()
        user_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "user_id": user_id,
        "name": name,
        "email": email
    })


@app.route("/profile", methods=["POST"])
def save_profile():
    data = request.get_json()
    user_id = data["user_id"]

    conn = sqlite3.connect("backend/placement_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM student_profile WHERE user_id = ?", (user_id,))
    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE student_profile
            SET branch=?, preferred_role=?, cgpa=?, coding_score=?, dsa_solved=?,
                projects=?, internships=?, communication_score=?, aptitude_score=?
            WHERE user_id=?
        """, (
            data["branch"], data.get("preferred_role", ""), data["cgpa"], data["coding_score"],
            data["dsa_solved"], data["projects"], data["internships"],
            data["communication_score"], data["aptitude_score"], user_id
        ))
    else:
        cursor.execute("""
            INSERT INTO student_profile
            (user_id, branch, preferred_role, cgpa, coding_score, dsa_solved, projects, internships, communication_score, aptitude_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, data["branch"], data.get("preferred_role", ""), data["cgpa"], data["coding_score"],
            data["dsa_solved"], data["projects"], data["internships"],
            data["communication_score"], data["aptitude_score"]
        ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Profile saved successfully"})


@app.route("/profile/<int:user_id>", methods=["GET"])
def get_profile(user_id):
    conn = sqlite3.connect("backend/placement_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT branch, preferred_role, cgpa, coding_score, dsa_solved, projects, internships, communication_score, aptitude_score
        FROM student_profile WHERE user_id = ?
    """, (user_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"exists": False})

    return jsonify({
        "exists": True,
        "branch": row[0],
        "preferred_role": row[1],
        "cgpa": row[2],
        "coding_score": row[3],
        "dsa_solved": row[4],
        "projects": row[5],
        "internships": row[6],
        "communication_score": row[7],
        "aptitude_score": row[8]
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    input_data = pd.DataFrame([{
        "CGPA": data["CGPA"],
        "CodingScore": data["CodingScore"],
        "DSASolved": data["DSASolved"],
        "Projects": data["Projects"],
        "Internships": data["Internships"],
        "CommunicationScore": data["CommunicationScore"],
        "AptitudeScore": data["AptitudeScore"]
    }])

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0]
    placed_index = list(model.classes_).index("Placed")
    placement_probability = round(probability[placed_index] * 100, 2)

    if placement_probability >= 75:
        readiness = "High"
    elif placement_probability >= 50:
        readiness = "Medium"
    else:
        readiness = "Low"

    guidance = []
    if data["CGPA"] < 7:
        guidance.append(f"Your CGPA is {data['CGPA']}. Try to raise it above 7.0, as it plays an important role in placements.")
    if data["CodingScore"] < 60:
        guidance.append(f"Your coding score is {data['CodingScore']}/100. Practice more on platforms like LeetCode or HackerRank to cross 60.")
    if data["DSASolved"] < 150:
        guidance.append(f"You've solved {data['DSASolved']} DSA problems. Aim for at least 150 to strengthen your fundamentals.")
    if data["CommunicationScore"] < 60:
        guidance.append(f"Your communication score is {data['CommunicationScore']}/100. Practice mock interviews and group discussions to improve it.")
    if data["Projects"] < 2:
        guidance.append(f"You currently have {data['Projects']} project(s). Try building at least 2-3 solid projects to showcase on your resume.")
    if data["Internships"] == 0:
        guidance.append("You haven't done an internship yet. Completing even one internship can significantly strengthen your resume.")
    if data["AptitudeScore"] < 60:
        guidance.append(f"Your aptitude score is {data['AptitudeScore']}/100. Regular practice of quantitative and logical reasoning can help.")

    if len(guidance) == 0:
        guidance.append(f"With a CGPA of {data['CGPA']} and strong scores across the board, you are well prepared. Keep practicing interviews and stay consistent.")

    conn = sqlite3.connect("backend/placement_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO student_predictions 
        (CGPA, CodingScore, DSASolved, Projects, Internships, CommunicationScore, AptitudeScore, PredictionResult)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["CGPA"], data["CodingScore"], data["DSASolved"], data["Projects"],
        data["Internships"], data["CommunicationScore"], data["AptitudeScore"], prediction
    ))
    conn.commit()
    conn.close()

    return jsonify({
        "PlacementPrediction": prediction,
        "PlacementProbability": placement_probability,
        "Readiness": readiness,
        "Guidance": guidance
    })


@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()

    recommendations = recommend_roles(
        coding_score=data["CodingScore"],
        dsa_solved=data["DSASolved"],
        aptitude_score=data["AptitudeScore"],
        communication_score=data["CommunicationScore"],
        branch=data.get("Branch")
    )

    top_role = recommendations[0]["RoleName"] if len(recommendations) > 0 else None
    skill_gap = get_skill_gap(top_role) if top_role else []

    return jsonify({
        "RecommendedRoles": recommendations,
        "SkillGap": skill_gap
    })


if __name__ == "__main__":
    app.run(debug=True)