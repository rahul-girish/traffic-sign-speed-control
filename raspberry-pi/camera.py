import cv2
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
        
        resized_frame = cv2.resize(frame, (640, 200), interpolation=cv2.INTER_AREA)
        cv2.imshow("Raspberry Pi Webcam", resized_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()