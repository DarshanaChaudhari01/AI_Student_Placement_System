import sqlite3

def create_database():
    conn = sqlite3.connect("backend/placement_data.db")
    cursor = conn.cursor()

    # Purana table (predictions ke liye)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            CGPA REAL,
            CodingScore INTEGER,
            DSASolved INTEGER,
            Projects INTEGER,
            Internships INTEGER,
            CommunicationScore INTEGER,
            AptitudeScore INTEGER,
            PredictionResult TEXT
        )
    """)

    # Naya table: Users (login ke liye)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )
    """)

    # Naya table: Student Profile
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            branch TEXT,
            preferred_role TEXT,
            cgpa REAL,
            coding_score INTEGER,
            dsa_solved INTEGER,
            projects INTEGER,
            internships INTEGER,
            communication_score INTEGER,
            aptitude_score INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    conn.commit()
    conn.close()
    print("Database aur saare tables successfully ban gaye!")

if __name__ == "__main__":
    create_database()