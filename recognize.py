import cv2
import os
import numpy as np
import csv
from datetime import datetime

dataset_path = "dataset"

faces = []
labels = []
label_names = {}

current_label = 0

# Load registered faces
for folder_name in os.listdir(dataset_path):

    folder_path = os.path.join(dataset_path, folder_name)

    if not os.path.isdir(folder_path):
        continue

    label_names[current_label] = folder_name

    for image_name in os.listdir(folder_path):

        image_path = os.path.join(folder_path, image_name)

        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is not None:
            faces.append(image)
            labels.append(current_label)

    current_label += 1


if len(faces) == 0:
    print("No registered faces found!")
    exit()


# Create LBPH face recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.train(faces, np.array(labels))

print("Face recognition model trained successfully!")
print("Starting camera...")


# Load Haar Cascade
cascade_path = os.path.join(
    os.path.dirname(__file__),
    "haarcascade_frontalface_default.xml"
)

face_detector = cv2.CascadeClassifier(cascade_path)


if face_detector.empty():
    print("Face detector file not found!")
    exit()


# Attendance file
attendance_file = "attendance.csv"
marked_today = set()

today = datetime.now().strftime("%Y-%m-%d")

if os.path.exists(attendance_file):
    with open(attendance_file, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["Date"] == today:
                marked_today.add(row["Roll No"]) 

if not os.path.exists(attendance_file):
    with open(attendance_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Roll No", "Name", "Date", "Time", "Status"])


# Start camera
camera = cv2.VideoCapture(0)


while True:

    ret, frame = camera.read()

    if not ret:
        print("Camera not detected!")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detected_faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in detected_faces:

        face = gray[y:y+h, x:x+w]

        label, confidence = recognizer.predict(face)

        if confidence < 100:

            name = label_names[label]
            text = name

            roll_no = name.split("_")[0]
            student_name = name.split("_", 1)[1]

            today = datetime.now().strftime("%Y-%m-%d")

            if roll_no not in marked_today:

                current_time = datetime.now().strftime("%H:%M:%S")

                with open(attendance_file, "a", newline="") as file:
                    writer = csv.writer(file)

                    writer.writerow([
                        roll_no,
                        student_name,
                        today,
                        current_time,
                        "Present"
                    ])

                marked_today.add(roll_no)

                print(
                    f"Attendance marked: {roll_no} - {student_name}"
                )

        else:

            text = "Unknown"


        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            text,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )


    cv2.imshow("Face Recognition", frame)


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


camera.release()
cv2.destroyAllWindows()