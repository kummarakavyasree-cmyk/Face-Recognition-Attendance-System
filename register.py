import cv2
import os

name = input("Enter student name: ")
roll_no = input("Enter roll number: ")

folder_name = f"{roll_no}_{name}"
folder_path = os.path.join("dataset", folder_name)

os.makedirs(folder_path, exist_ok=True)

camera = cv2.VideoCapture(0)

count = 0

print("Camera starting...")
print("Look at the camera. Press Q to stop.")

while True:
    ret, frame = camera.read()

    if not ret:
        print("Camera not detected!")
        break

    cv2.imshow("Register Student", frame)

    if count < 20:
        image_path = os.path.join(folder_path, f"{count + 1}.jpg")
        cv2.imwrite(image_path, frame)
        count += 1
        print(f"Captured image {count}/20")

    if count >= 20:
        print("Registration completed!")
        break

    if cv2.waitKey(100) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()