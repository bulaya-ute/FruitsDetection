import serial
from time import sleep

# Replace 'COM3' with the appropriate port for your Arduino
# For Linux or macOS, it could be something like '/dev/ttyUSB0' or '/dev/ttyACM0'
arduino_port = 'COM3'  # Change this to your port
baud_rate = 9600  # The baud rate should match the one set in the Arduino sketch


def send_command(command: str):
    ser.write(command.encode())
    print(f"Response: {ser.readline().decode().strip()}")


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


try:
    # Initialize the serial connection
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)

    # Give the connection a second to settle
    sleep(2)

    # Test the pickMotion function
    pickMotion()

finally:
    # Close the serial connection
    ser.close()
