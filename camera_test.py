import cv2

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()

    if not ret:
        print("Camera not detected")
        break

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()