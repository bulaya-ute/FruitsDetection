import serial
import time

# Initialize serial connection to Arduino
arduino = serial.Serial(port='COM8', baudrate=9600, timeout=.1)


def send_command(_command: str):
    try:
        arduino.write(f"{_command}\n".encode())
        print(f"Sent: {_command}")
        # Wait for the Arduino to process the command and respond
        time.sleep(0.5)  # Adjust the delay as needed
        read_response()
    except serial.SerialException as e:
        print(f"Error sending command: {e}")


def read_response():
    try:
        if arduino.in_waiting > 0:
            response = arduino.readline().decode().strip()
            print(f"Arduino response: {response}")
        else:
            print("Arduino response: ")
    except serial.SerialException as e:
        print(f"Error reading response: {e}")


# Example commands to test each motor
commands = [
    "motorA(30)",
    "motorB(45)",
    "motorC(60)",
    "motorD(90)",
    "motorE(120)",
    "motorF(150)"
]

# # Send predefined commands with a delay
# for command in commands:
#     send_command(command)
#     time.sleep(1)  # Wait for 1 second between commands

# Continuously prompt for user input and send commands to Arduino
while True:
    command = input("Enter command (or 'exit' to quit): ")
    if command.lower() == 'exit':
        break
    send_command(command)
