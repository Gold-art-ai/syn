import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib

# Load collected data
df = pd.read_csv("face_data.csv")

# Separate features and labels
X = df.drop(columns=["label"]).values
y = df["label"].values

# Encode labels
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Normalize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train the classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_scaled, y_encoded)

# Save the model and encoders
joblib.dump(clf, "face_model.pkl")
joblib.dump(label_encoder, "face_label_encoder.pkl")
joblib.dump(scaler, "face_scaler.pkl")

print(" Model trained and saved!")
