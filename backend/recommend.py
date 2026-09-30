import pandas as pd

def calculate_role_difficulty():
    roles = pd.read_csv("dataset/roles.csv")
    role_skills = pd.read_csv("dataset/role_skills.csv")
    skills = pd.read_csv("dataset/skills.csv")
    skills["SkillID"] = skills.index + 1
    merged = role_skills.merge(skills, on="SkillID")
    role_difficulty = merged.groupby("RoleID")["DifficultyWeight"].mean().reset_index()
    role_difficulty.columns = ["RoleID", "AvgDifficulty"]
    role_difficulty = role_difficulty.merge(roles, on="RoleID")
    return role_difficulty


# Branch ke hisaab se relevant RoleType map karte hain
BRANCH_ROLE_MAP = {
    "Computer Science": ["Software", "Analytics"],
    "Information Technology": ["Software", "Analytics"],
    "Data Science": ["Analytics", "Software"],
    "Artificial Intelligence": ["Software", "Analytics"],
    "Artificial Intelligence & ML": ["Software", "Analytics"],
    "Electronics with Software Focus": ["Software", "Electronics"],
}


def recommend_roles(coding_score, dsa_solved, aptitude_score, communication_score, top_n=3, branch=None):
    role_difficulty = calculate_role_difficulty()

    relevant_types = BRANCH_ROLE_MAP.get(branch, ["Software", "Analytics"])
    role_difficulty = role_difficulty[role_difficulty["RoleType"].isin(relevant_types)]

    # Branch ka primary focus area — us type ke roles ko strictly priority dete hain
    priority_type = None
    if branch == "Data Science":
        priority_type = "Analytics"
    elif branch == "Electronics with Software Focus":
        priority_type = "Electronics"

    if priority_type:
        priority_roles = role_difficulty[role_difficulty["RoleType"] == priority_type]
        if len(priority_roles) >= top_n:
            role_difficulty = priority_roles

    student_skill_level = (
        (coding_score / 100) * 2 +
        (dsa_solved / 400) * 2 +
        (aptitude_score / 100) * 0.5 +
        (communication_score / 100) * 0.5
    )

    role_difficulty = role_difficulty.copy()
    role_difficulty["Distance"] = abs(role_difficulty["AvgDifficulty"] - student_skill_level)
    recommended = role_difficulty.sort_values("Distance").head(top_n)

    return recommended[["RoleName", "RoleType", "AvgDifficulty"]].to_dict(orient="records")


def get_skill_gap(role_name):
    roles = pd.read_csv("dataset/roles.csv")
    role_skills = pd.read_csv("dataset/role_skills.csv")
    skills = pd.read_csv("dataset/skills.csv")
    skills["SkillID"] = skills.index + 1

    role_row = roles[roles["RoleName"] == role_name]
    if role_row.empty:
        return []

    role_id = role_row.iloc[0]["RoleID"]
    required_skill_ids = role_skills[role_skills["RoleID"] == role_id]["SkillID"]
    required_skills = skills[skills["SkillID"].isin(required_skill_ids)]
    top_skills = required_skills.sort_values("DifficultyWeight", ascending=False).head(5)

    return top_skills["SkillName"].tolist()


if __name__ == "__main__":
    result = recommend_roles(coding_score=85, dsa_solved=300, aptitude_score=75, communication_score=80, branch="Data Science")
    print(result)