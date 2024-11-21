import subprocess
import socket
import time

def handle_messages():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("192.168.0.56", 31337))
        s.listen()
        c_socket, c_address = s.accept()
        print(f"Connection from {c_address}")

        process_variable = False
        while True:
            received = c_socket.recv(1024)
            message = received.decode()
            if message:
                print(f"Message: {message}")

                # Choose an option based on message
                if message.startswith("Answer:"):
                    with open("answer.txt", "a") as file:
                        answer = message[len("Answer:"):]
                        file.write(answer + '\n')

                elif message == "START_CAPTURE":
                    print("START_CAPTURE...")
                    process_variable = subprocess.Popen(["airodump-ng", "--channel","36", "--bssid", "04:F0:21:1B:61:BA", "--write", "capture", "wlp0s20f3mon"])

                elif message == "STOP_CAPTURE":
                    print("STOP_CAPTURE...")
                    process_variable.terminate()

                elif message == "STOP_SCRIPT":
                    print("STOP_SCRIPT...")
                    break

if __name__ == '__main__':
    handle_messages()
