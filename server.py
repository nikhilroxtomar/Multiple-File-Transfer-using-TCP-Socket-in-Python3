
import os
import socket

IP = "127.0.0.1"
PORT = 4456
SIZE = 1024
FORMAT = "utf"
SERVER_FOLDER = "server_folder"

def main():
    print("[STARTING] Server is starting.\n")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP, PORT))
    server.listen()
    print("[LISTENING] Server is waiting for clients.")

    while True:
        conn, addr = server.accept()
        print(f"[NEW CONNECTION] {addr} connected.\n")

        """ Receiving the folder_name """
        folder_name = conn.recv(SIZE).decode(FORMAT)

        """ Creating the folder """
        folder_path = os.path.join(SERVER_FOLDER, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            conn.send(f"Folder ({folder_name}) created.".encode(FORMAT))
        else:
            conn.send(f"Folder ({folder_name}) already exists.".encode(FORMAT))

        """ Receiving files """
        while True:
            msg = conn.recv(SIZE).decode(FORMAT)
            cmd, data = msg.split(":")

            if cmd == "FILENAME":
                """ Recv the file name """
                print(f"[CLIENT] Received the filename: {data}.")

                file_path = os.path.join(folder_path, data)
                file = open(file_path, "w")
                conn.send("Filename received.".encode(FORMAT))

            elif cmd == "DATA":
                """ Recv data from client """
                print(f"[CLIENT] Receiving the file data.")
                file.write(data)
                conn.send("File data received".encode(FORMAT))

            elif cmd == "FINISH":
                file.close()
                print(f"[CLIENT] {data}.\n")
                conn.send("The data is saved.".encode(FORMAT))

            elif cmd == "CLOSE":
                conn.close()
                print(f"[CLIENT] {data}")
                break

if __name__ == "__main__":
    main()
