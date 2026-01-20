import time
from camera import stream

print("Raspberry Pi module is running.")

def main():
    
    stream()
    
    try:
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Stopping.")
        

if __name__ == "__main__":
    
    main()