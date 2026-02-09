import sys
import tty
import termios
import time
from camera import stream
from gpiozero import RotaryEncoder, PWMOutputDevice, OutputDevice

# Pins
ENA = 12
IN1 = 17
IN2 = 27

# Motor
motor_pwm = PWMOutputDevice(ENA)
pin_in1 = OutputDevice(IN1)
pin_in2 = OutputDevice(IN2)

yolo_speed_limit = 120.0
manual_input_speed = 0.0
STEP_SIZE = 5

def update_motor():
    effective_speed = min(manual_input_speed, yolo_speed_limit)
    
    pin_in1.on()
    pin_in2.off()
    
    motor_pwm.value = effective_speed / 120.0
    
    print(f"Set speed to {effective_speed}")

def handle_new_speed(speed):
    global yolo_speed_limit
    try:
        yolo_speed_limit = float(speed)
        update_motor()
        print(f"\nNew Speed Limit Set: {yolo_speed_limit} km/h")
    except ValueError:
        pass

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
        
def main():
    global manual_input_speed
    stream(handle_new_speed)
    
    print("Use W/S to adjust speed")
    try:
        while True:
            char = get_key().lower()
            
            if char == 'w':
                manual_input_speed = min(120.0, manual_input_speed + STEP_SIZE)
                update_motor()
            elif char == 's':
                manual_input_speed = max(0.0, manual_input_speed - STEP_SIZE)
                update_motor()
            elif char == ' ':
                manual_input_speed = 0.0
                update_motor()
            elif char == 'q':
                print("Quitting")
                break
                
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        pass
    finally:
        print("Stopping.")
        motor_pwm.value = 0
        pin_in1.off()
        pin_in2.off()
        

if __name__ == "__main__":
    
    print("Raspberry Pi module is running.")
    main()
