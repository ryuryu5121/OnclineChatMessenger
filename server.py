import socket
import threading

sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = '0.0.0.0'
tcp_server_port = 9001
udp_server_port = 9002

print('starting up on port {}'.format(tcp_server_port))

sock_tcp.bind((server_address, tcp_server_port))
sock_udp.bind((server_address, udp_server_port))
sock_tcp.listen(10)

chat_rooms = {}
token = ""

def connect_client():
    print('wait connect')
    while True:
        connection, client_address = sock_tcp.accept()
        try:
            header = connection.recv(33)
            room_name_length = int.from_bytes(header[:1], "big")
            operation = int.from_bytes(header[1:2], "big")
            port = int.from_bytes(header[2:4], "big")
            operation_pay_load_size = int.from_bytes(header[4:33], "big")

            room_name = connection.recv(room_name_length).decode("utf-8")
            user_name = connection.recv(operation_pay_load_size).decode("utf-8")
            
            address = '0.0.0.0'
            print(client_address)
            token = f'{address}:{port}'

            client = Client(user_name, address, port)

            if operation == 1:
                chat_room = ChatRoom(room_name, token)
                chat_room.add_member(client, token)
                chat_rooms[room_name] = chat_room
                message_to_client = 'you make a new room: ' + room_name
                print(user_name)
                print(message_to_client)
            
            if operation == 2:
                chat_rooms[room_name].add_member(client, token)
                message_to_client = 'you join ' + room_name
                print(message_to_client)
            
        except Exception as e:
            print(f"Error receiving message from server: {e}")
            break

        finally:
            message_len = len(message_to_client).to_bytes(1, "big")
            token_size = len(token).to_bytes(1, "big")
            print(len(message_to_client))
            print("token: " + token)
            print(len(token))
            connection.send(message_len + token_size)
            connection.send(message_to_client.encode("utf-8") + token.encode('utf-8'))
            connection.close()
            print('closing tcp')

class Client:
    def __init__(self, user_name, address, port):
        self.name = user_name
        self.address = address
        self.port = port
    
class ChatRoom:
    def __init__(self, room_name, token):
        self.members = {}
        self.room_name = room_name
        self.host_token = token
    
    def add_member(self, member, token):
        self.members[token] = member
    
def handle_with_message():
    while True:
        print('\nwaiting to receive message')
        data, server = sock_udp.recvfrom(2)

        if data is None:
            break

        print("get data")
        room_name_length = int.from_bytes(data[:1], "big")
        print(room_name_length)
        token_size = int.from_bytes(data[1:2], "big")
        print(token_size)
        data, server = sock_udp.recvfrom(4094)
        room_name = data[0:room_name_length].decode('utf-8')
        print(room_name)
        token = data[room_name_length:room_name_length + token_size].decode('utf-8')
        message_from_client = data[room_name_length + token_size:]
        print(message_from_client.decode('utf-8'))
        print(chat_rooms[room_name].members)


        if token in chat_rooms[room_name].members:
            send_user = chat_rooms[room_name].members[token]
            send_user_name = send_user.name
            send_user_name_length = len(send_user_name).to_bytes(1, "big")
            for key, value in chat_rooms[room_name].members.items():
                if key != token:
                    send = sock_udp.sendto(send_user_name_length, (value.address, value.port))
                    print("name_length: {}".format(send_user_name_length))
                    print("port: {}".format(value.port) )
                    print("send {}".format(send))
                    send = sock_udp.sendto(send_user_name.encode('utf-8') + message_from_client, (value.address, value.port))
                    print("send {}".format(send))
                    print("send message ")


connect_client_thread = threading.Thread(target=connect_client, args=())
connect_client_thread.start()
handle_with_message_thread = threading.Thread(target=handle_with_message, args=())
handle_with_message_thread.start()



# while True:
#     print('\nwaiting to receive message')

#     data, server = sock_udp.recvfrom(4096)
#     room_name_length = int.from_bytes(data[:1], "big")
#     operation = int.from_bytes(data[1:2], "big")
#     state = int.from_bytes(data[2:3], "big")
#     operation_pay_load_size = int.from_bytes(data[3:])
#     room_name = data[3: room_name_length + 3].decode('utf-8')
#     operation_pay_load = data[room_name_length + 3: room_name_length + 3]
    

#     print('Received header from client. Byte lengths: Title length {}'.format(name_length))

    # user_name = data[1:name_length + 1].decode('utf-8')
    # message = data[name_length + 1:].decode('utf-8')
    # print("{}: {} ".format(user_name, message))

    # for client in clients:
    #     if client != server:
    #         sent = sock.sendto(data, client)
    #         print('sent {} bytes back to {}'.format(sent, client))

