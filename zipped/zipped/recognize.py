import cv2
import mediapipe as mp
import numpy as np
import joblib

# Load model and encoders
clf = joblib.load("face_model.pkl")
label_encoder = joblib.load("face_label_encoder.pkl")
scaler = joblib.load("face_scaler.pkl")

# Set confidence threshold
UNKNOWN_THRESHOLD = 0.5  # tune this value as needed

# Initialize FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh()

# Webcam
cap = cv2.VideoCapture(0)

print("🎥 Running face recognition...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)
    label = "No Face"

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            landmarks = []
            for lm in face_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
            
            if len(landmarks) == 1404:  # 468 points * 3
                landmarks_np = np.array(landmarks).reshape(1, -1)
                landmarks_scaled = scaler.transform(landmarks_np)

                # Predict probabilities
                probs = clf.predict_proba(landmarks_scaled)[0]
                max_prob = np.max(probs)
                pred_idx = np.argmax(probs)

                if max_prob < UNKNOWN_THRESHOLD:
                    label = "Unknown"
                else:
                    label = label_encoder.inverse_transform([pred_idx])[0]

    # Show prediction
    cv2.putText(frame, f"Detected: {label}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
