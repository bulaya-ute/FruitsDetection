import cv2
import numpy as np
import serial
from time import sleep

# Replace 'COM7' with the appropriate port for your Arduino
arduino_port = 'COM7'  # Change this to your port
baud_rate = 9600  # The baud rate should match the one set in the Arduino sketch

# Initialize the serial connection
ser = serial.Serial(arduino_port, baud_rate, timeout=1)
# Give the connection a second to settle
sleep(2)


def send_command(command: str):
    sleep(4)
    ser.write(command.encode())
    print(f"Command sent: {command}  ", end="")
    while True:
        if ser.in_waiting > 0:
            response = ser.readline().decode().strip()
            print(f"Response: {response}")
            return response



def initialPos():
    send_command("motorA(0)")  # BASE
    send_command("motorB(60)")
    send_command("motorC(160)")
    send_command("motorD(20)")
    send_command("motorE(120)")  # wrist
    send_command("openGrip")  # claw: 30 = open, 85 = closed
    send_command("motorG(10)")


def pickMotion():
    send_command("motorA(90)")  # Base position
    sleep(1)

    send_command("motorB(60)")  # Adjust arm position
    sleep(1)

    send_command("motorC(160)")  # Adjust arm position
    sleep(1)

    send_command("motorD(20)")  # Adjust arm position
    sleep(1)

    send_command("motorE(120)")  # Adjust wrist position
    sleep(1)

    send_command("openGrip")  # Open gripper
    sleep(1)


def place_motion():
    send_command("motorA(0)")
    sleep(1)
    send_command("motorB(60)")
    sleep(1)
    send_command("motorC(175)")
    sleep(1)
    send_command("motorD(20)")
    sleep(1)
    send_command("motorE(120)")
    sleep(1)
    send_command("closeGrip")
    sleep(1)


def is_approximately_red(mean_color):
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    return np.all(lower_red <= mean_color) and np.all(mean_color <= upper_red)


# Initialize the camera
cap = cv2.VideoCapture(0)
center = (320, 240)
radius = 50

try:
    # initialPos()
    # sleep(3)
    #
    # while True:
    #     ret, frame = cap.read()
    #     if not ret:
    #         break
    #
    #     # Draw a square at the center of the frame
    #     top_left = (center[0] - radius, center[1] - radius)
    #     bottom_right = (center[0] + radius, center[1] + radius)
    #     cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)
    #
    #     # Extract the region of interest (ROI)
    #     roi = frame[center[1] - radius:center[1] + radius, center[0] - radius:center[0] + radius]
    #
    #     # Convert the ROI to HSV color space
    #     hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    #     mean_color = np.mean(hsv_roi, axis=(0, 1))
    #
    #     # Check if the mean color is approximately red
    #     if is_approximately_red(mean_color):
    #         pickMotion()
    #
    #     cv2.imshow('Frame', frame)
    #
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break

    while True:
        com = input("Enter command: ")
        if com == "initial":
            initialPos()
        elif com.lower() == "pick":
            pickMotion()
        elif com.lower() == "place":
            place_motion()
        else:
            send_command(com)

finally:
    # Release the camera and close the serial connection
    cap.release()
    ser.close()
    cv2.destroyAllWindows()
