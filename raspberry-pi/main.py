import time
from camera import stream

def handle_new_speed(speed):
    
    return None

def main():
    
    stream(handle_new_speed)
    
    try:
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Stopping.")
        

if __name__ == "__main__":
    
    print("Raspberry Pi module is running.")
    main()