import pandas as pd
import numpy as np
import random

# Random seed set karte hain taaki data generate karne par
# hamesha same numbers milein (reproducibility ke liye)
np.random.seed(42)
random.seed(42)

# Kitne dummy students banane hain
NUM_STUDENTS = 500

print("Student data generate hone wala hai...")
# Branches (humare branches file ke hisaab se BranchID 1,2,3... use kar rahe hain)
# Abhi ke liye maan lete hain 5 branches hain
BRANCH_IDS = [1, 2, 3, 4, 5]

# Roles jo roles.csv mein the (1 se 16 tak)
ROLE_IDS = list(range(1, 17))

students_data = []

for i in range(1, NUM_STUDENTS + 1):
    student_id = 3000 + i
    name = f"Student_{i}"
    gender = random.choice(["Male", "Female"])
    email = f"student{i}@example.com"
    phone = f"9{random.randint(100000000, 999999999)}"
    branch_id = random.choice(BRANCH_IDS)

    cgpa = round(random.uniform(5.5, 9.8), 2)
    coding_score = random.randint(20, 100)
    dsa_solved = random.randint(0, 400)
    projects = random.randint(0, 6)
    internships = random.randint(0, 3)
    communication_score = random.randint(30, 100)
    aptitude_score = random.randint(30, 100)
    preferred_role_id = random.choice(ROLE_IDS)

    # Ek simple "score" banate hain jo decide karega placement ka chance
    placement_score = (
        (cgpa / 10) * 30 +
        (coding_score / 100) * 25 +
        (dsa_solved / 400) * 20 +
        (projects / 6) * 10 +
        (internships / 3) * 10 +
        (communication_score / 100) * 5
    )

    # Agar score threshold se upar hai to zyada chance "Placed" ka
    placement_status = "Placed" if placement_score > 55 else "Not Placed"

    students_data.append({
        "StudentID": student_id,
        "Name": name,
        "Gender": gender,
        "Email": email,
        "Phone": phone,
        "BranchID": branch_id,
        "CGPA": cgpa,
        "CodingScore": coding_score,
        "DSASolved": dsa_solved,
        "Projects": projects,
        "Internships": internships,
        "CommunicationScore": communication_score,
        "AptitudeScore": aptitude_score,
        "PreferredRoleID": preferred_role_id,
        "PlacementStatus": placement_status
    })

print(f"{len(students_data)} students ka data ban gaya (placement status ke saath)")

# Ab is data ko pandas DataFrame mein convert karke CSV file mein save karenge
df = pd.DataFrame(students_data)
df.to_csv("dataset/students.csv", index=False)

print("students.csv file save ho gayi!")
print(df["PlacementStatus"].value_counts())