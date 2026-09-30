import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# Step 1: Dataset load karo
df = pd.read_csv("dataset/students.csv")

print("Total records:", len(df))
print("\nColumns:", list(df.columns))

print("\nPehle 5 rows:")
print(df.head())

print("\nMissing values check:")
print(df.isnull().sum())


# Step 2: Features aur target select karo
feature_columns = [
    "CGPA",
    "CodingScore",
    "DSASolved",
    "Projects",
    "Internships",
    "CommunicationScore",
    "AptitudeScore"
]

X = df[feature_columns]
y = df["PlacementStatus"]

print("\nFeatures shape:", X.shape)
print("Target shape:", y.shape)


# Step 3: Training aur testing data split karo
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("\nTraining data size:", X_train.shape)
print("Testing data size:", X_test.shape)


# Step 4: Random Forest model banao
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Model train karo
model.fit(X_train, y_train)

print("\nModel training complete!")


# Step 5: Model ki accuracy check karo
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(f"\nModel Accuracy: {accuracy * 100:.2f}%")


# Step 6: Classification Report
print("\nDetailed Classification Report:")

print(classification_report(y_test, y_pred))


# Step 7: Feature Importance calculate karo
importances = model.feature_importances_

feature_importance = pd.DataFrame({
    "Feature": feature_columns,
    "Importance": importances
})

feature_importance = feature_importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance:")
print(feature_importance.to_string(index=False))


# Step 8: 5-Fold Cross-Validation
print("\n5-Fold Cross-Validation:")

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

cv_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

cv_scores = cross_val_score(
    cv_model,
    X,
    y,
    cv=cv,
    scoring="accuracy"
)

print("\nAccuracy of each fold:")
for i, score in enumerate(cv_scores, start=1):
    print(f"Fold {i}: {score * 100:.2f}%")

print(f"\nAverage Cross-Validation Accuracy: {cv_scores.mean() * 100:.2f}%")
print(f"Standard Deviation: {cv_scores.std() * 100:.2f}%")


# Step 9: Model save karo
joblib.dump(model, "model/placement_model.pkl")

print("\nModel successfully saved!")
print("Location: model/placement_model.pkl")