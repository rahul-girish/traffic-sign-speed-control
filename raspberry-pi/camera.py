import cv2
from flask import Flask, Response
import threading
import config

def capture_video():
    ''' None -> None
    
    Captures video from the webcam using OpenCV and displays the video in a window.
    '''
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_FPS, config.FPS)
    
    print("Press 'q' to quit.")
    
    while True:
        
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Can't receive frame.")
            break
        
        frame = cv2.resize(frame, (config.RESIZED_WIDTH, config.RESIZED_HEIGHT), interpolation=cv2.INTER_AREA)
        cv2.imshow("Raspberry Pi Webcam", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    

app = Flask(__name__)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()
        
cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
cap.set(cv2.CAP_PROP_FPS, config.FPS)

def generate_frames():
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.resize(frame, (config.RESIZED_WIDTH, config.RESIZED_HEIGHT))
        ret, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        
        
@app.route('/')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def start_stream():
    app.run(host='0.0.0.0', port=config.PORT, debug=False, use_reloader=False)
    
def stream():
    
    thread = threading.Thread(target=start_stream)
    thread.daemon = True
    thread.start()
    print(f"Stream started at http://{config.RASPBERRY_PI_IP}:5000")