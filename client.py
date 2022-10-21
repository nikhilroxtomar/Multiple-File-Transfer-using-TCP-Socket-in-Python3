
import os
import socket

IP = "127.0.0.1"
PORT = 4456
SIZE = 1024
FORMAT = "utf"
CLIENT_FOLDER = "client_folder"

def main():
    """ Starting a tcp socket """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))

    """ Folder path """
    path = os.path.join(CLIENT_FOLDER, "files")
    folder_name = path.split("/")[-1]

    """ Sending the folder name """
    msg = f"{folder_name}"
    print(f"[CLIENT] Sending folder name: {folder_name}")
    client.send(msg.encode(FORMAT))

    """ Receiving the reply from the server """
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER] {msg}\n")

    """ Sending files """
    files = sorted(os.listdir(path))

    for file_name in files:
        """ Send the file name """
        msg = f"FILENAME:{file_name}"
        print(f"[CLIENT] Sending file name: {file_name}")
        client.send(msg.encode(FORMAT))

        """ Recv the reply from the server """
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")

        """ Send the data """
        file = open(os.path.join(path, file_name), "r")
        file_data = file.read()

        msg = f"DATA:{file_data}"
        client.send(msg.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")

        """ Sending the close command """
        msg = f"FINISH:Complete data send"
        client.send(msg.encode(FORMAT))
        msg = client.recv(SIZE).decode(FORMAT)
        print(f"[SERVER] {msg}")

    """ Closing the connection from the server """
    msg = f"CLOSE:File transfer is completed"
    client.send(msg.encode(FORMAT))
    client.close()




if __name__ == "__main__":
    main()
