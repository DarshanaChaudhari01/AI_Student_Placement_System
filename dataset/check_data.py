import pandas as pd

# Dono files load karo
students = pd.read_csv("dataset/students.csv")
placements = pd.read_csv("dataset/placements.csv")

# Dono files ke StudentID ki list nikalo
student_ids_in_students_file = set(students["StudentID"])
student_ids_in_placements_file = set(placements["StudentID"])

# Kitne placements records hain jinke StudentID students.csv mein maujood hain
matching = student_ids_in_placements_file.intersection(student_ids_in_students_file)
not_matching = student_ids_in_placements_file - student_ids_in_students_file

print(f"Total students.csv mein: {len(student_ids_in_students_file)}")
print(f"Total unique StudentID placements.csv mein: {len(student_ids_in_placements_file)}")
print(f"Match ho rahe StudentID: {len(matching)}")
print(f"Match NAHI ho rahe StudentID: {len(not_matching)}")