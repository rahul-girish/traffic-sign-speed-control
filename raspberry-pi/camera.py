import cv2
from flask import Flask, Response, request
import threading
import config


app = Flask(__name__)
cap = cv2.VideoCapture(0)

on_speed_received = None

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

@app.route('/set_speed')
def set_speed():
    
    speed = request.args.get('value')
    if speed and on_speed_received:
        
        on_speed_received(speed)
        return f"Speed received: {speed}.", 200
    
    return "No speed received.", 400
def start_stream():
    app.run(host='0.0.0.0', port=config.PORT, debug=False, use_reloader=False)
    
def stream(callback_func):
    
    global on_speed_received
    on_speed_received = callback_func
    
    thread = threading.Thread(target=start_stream)
    thread.daemon = True
    thread.start()
    print(f"Stream started at http://{config.RASPBERRY_PI_IP}:5000")