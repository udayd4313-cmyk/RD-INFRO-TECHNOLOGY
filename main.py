import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


data = pd.read_csv("students.csv")


data["Gender"] = data["Gender"].map({"Male": 0, "Female": 1})


data["Result"] = data["Marks"].apply(lambda x: 1 if x >= 80 else 0)


X = data[["Age", "Gender"]]
y = data["Result"]


X = X.fillna(X.mean())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

print("Model trained successfully!")

new_student = pd.DataFrame({
    "Age": [20],
    "Gender": [0]    # 0 = Male, 1 = Female
})

prediction = model.predict(new_student)

if prediction[0] == 1:
    print("Prediction: Pass")
else:
    print("Prediction: Fail")