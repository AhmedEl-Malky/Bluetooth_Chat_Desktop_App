import socket


class Device:

    def __init__(self, my_mac_address, port, backlog, size):
        self.my_mac_address = my_mac_address  # The MAC address of a Bluetooth adapter on the server. The server
        # might have multiple Bluetooth adapters.
        self.port = port  # 3 is an arbitrary choice. However, it must match the port used by the client.
        self.backlog = backlog
        self.size = size
        self.client_socket = None
        self.bluetooth_socket = None
        self.channel = None

    def open_socket(self):
        self.bluetooth_socket = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)

    # for Server
    def open_connection(self):
        self.open_socket()

        # Bind the socket to the address and port
        self.bluetooth_socket.bind((self.my_mac_address, self.port))

        # Listen for incoming connections
        self.bluetooth_socket.listen(self.backlog)

        print("Server is listening for incoming connections...")

        # Accept incoming connection
        self.client_socket, client_address = self.bluetooth_socket.accept()
        # this use for send or receive data for server
        self.channel = self.client_socket
        print("Connection established with:", client_address)

    # for Client
    def connect_to_server(self, server_mac_address):
        self.open_socket()
        # Connect to the server
        self.bluetooth_socket.connect((server_mac_address, self.port))
        # this use for send or receive data for client
        self.channel = self.bluetooth_socket
    def close_connection(self):
        self.channel.close()
        self.bluetooth_socket.close()

    def send_file(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                data_send = file.read()
                self.channel.sendall(data_send)
                print("File sent successfully")
        except Exception as e:
            print("Error sending file:", e)

        finally:
            print("Closing socket")
            self.close_connection()

    def receive_file(self, save_path):
        try:
            # Receive a file from the server
            data = self.channel.recv(self.size)

            with open(save_path, 'wb') as file:
                file.write(data)
                print("File received and saved successfully")
        except Exception as e:
            print("Error receiving file:", e)
        finally:
            print("Closing socket")
            self.close_connection()

    # server establish  room
    def establish_room(self):
        while True:
            data = self.client_socket.recv(self.size).decode('utf-8')
            if data == 'break':
                self.close_connection()
                print('Chat Closed')
                break
            else:
                print('Received Data: ' + data)
                message = input('Enter your message: ')
                self.client_socket.send(message.encode('utf-8'))
                if message == 'break':
                    self.close_connection()
                    print('Chat Closed')
                    break

    # client enter room
    def enter_room(self):
        while True:
            message = input('Enter your message: ')
            self.bluetooth_socket.send(message.encode('utf-8'))
            if message == 'break':
                self.close_connection()

                print('Chat Closed')
                break
            data = self.bluetooth_socket.recv(self.size).decode('utf-8')
            if data == 'break':
                self.close_connection()
                print('Chat Closed')
                break
            print('Received Data: ' + data)