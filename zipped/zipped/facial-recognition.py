import cv2
import mediapipe as mp
import pandas as pd
import os

# Ask for label (name)
label = input("Enter your name (label): ").strip()

# Setup MediaPipe FaceMesh + Drawing
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# Webcam setup
cap = cv2.VideoCapture(0)
data = []

print("📸 Collecting face data with dots. Press 'q' to stop...\n")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and convert to RGB
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Draw dots (landmarks) on face
            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=drawing_spec,
                connection_drawing_spec=drawing_spec,
            )

            # Extract (x, y, z) coordinates of all 468 landmarks
            landmarks = []
            for lm in face_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])
            data.append(landmarks + [label])  # Add label

    # Show the frame
    cv2.putText(frame, f"Collecting for: {label}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Face Data Collection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()

# Save to CSV
csv_file = "face_data.csv"
df_new = pd.DataFrame(data)

# Create dynamic column names: f0, f1, ..., f1403 + label
num_landmarks = len(data[0]) - 1
columns = [f"f{i}" for i in range(num_landmarks)] + ["label"]
df_new.columns = columns

# Append or create
if os.path.exists(csv_file):
    df_existing = pd.read_csv(csv_file)
    df_all = pd.concat([df_existing, df_new], ignore_index=True)
else:
    df_all = df_new

df_all.to_csv(csv_file, index=False)
print(f"\n✅ Data saved to {csv_file} with label '{label}' and visible facial dots.")
