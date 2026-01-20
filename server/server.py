from ultralytics import YOLO
import cv2
import requests
import re
import config

last_sent_speed = None

def send_speed(speed=0):
    try:
        url = f"http://{config.RASPBERRY_PI_IP}:{config.PORT}/set_speed?value={speed}"
        response = requests.get(url, timeout=2)
        print(f"Sent speed {speed}, response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending speed: {e}")

# Load YOLOv8 model
detector = YOLO("./model/traffic_sign_detector.pt", task="detect")

cap = cv2.VideoCapture(config.STREAM_URL)

if not cap.isOpened():
    print("Could not open stream")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run detection on the frame
    detections = detector(frame)

    for detection in detections:
        class_ids = detection.boxes.cls
        for i, bbox in enumerate(detection.boxes):
            x1, y1, x2, y2 = bbox.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Get class label
            class_id = int(class_ids[i])
            class_name = detection.names[class_id]

            if class_name.startswith("Speed Limit"):
                match = re.search(r"\d+", class_name)
                if match:
                    speed_value = int(match.group())
                    print("Detected speed:", speed_value)
                    
                    if speed_value != last_sent_speed:
                        send_speed(speed_value)
                        last_sent_speed = speed_value

            # Draw class name
            cv2.putText(frame, class_name, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display frame
    cv2.imshow("Real-Time Detection", frame)

    # Exit on 'q'
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()