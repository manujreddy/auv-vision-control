import cv2
from ultralytics import YOLO
import os
from datetime import datetime

print("1. Loading YOLO model...")
model = YOLO("best.pt")

# Using 0 to access your laptop's default webcam
video_source = "sample_video.mp4"
print(f"2. Opening video source: {video_source}")
cap = cv2.VideoCapture(video_source)

if not cap.isOpened():
    print("ERROR: Could not open the webcam! Check permissions.")
    exit()

if not os.path.exists("Anomalies"):
    os.makedirs("Anomalies")

print("3. Starting video stream. Press 'q' on your keyboard to quit.")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("End of video stream.")
        break

    # Run YOLOv8 inference
    results = model(frame)
    annotated_frame = results[0].plot()

    # Event-Driven Recording Logic
    for box in results[0].boxes:
        if box.conf[0].item() > 0.70:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            cv2.imwrite(f"Anomalies/defect_{timestamp}.jpg", frame)
            print(f"CRITICAL: Defect logged at {timestamp}")

    # Show the video
    cv2.imshow("Underwater Vision Prototype", annotated_frame)

    # Press 'q' to quit
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
