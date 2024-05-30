import socket
import os
from faker import Faker

# ソケットの作成
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = '/tmp/socket_file'

# サーバーアドレスの準備
try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

sock.bind(server_address)
sock.listen(1)
print('Connection stated!')

# 通信の開始と終了
while True:
    connection, client_address = sock.accept()
    # データのデコードと表示
    try:
        while True:
            # 最大32バイトでデータを取得、utf-8を指定しデコード　
            data = connection.recv(32)
            data_str = data.decode('utf-8')
            print('Recieved data >>>', data_str)

            # Fakerインスタンスの作成
            if data_str == "us":
                fake = Faker('en_US')
            elif data_str == "jp":
                fake = Faker('ja_JP')
            elif data_str == "it":
                fake = Faker('it_IT')
            
            # データの加工
            if data:
                name = fake.name()
                address = fake.address().replace('\n', ', ')
                email = fake.email()
                response_str = f"Name: {name}, Address: {address}, Email: {email}"
                response_bytes = response_str.encode('utf-8')
                connection.sendall(response_bytes)
            else:
                print('Do not exist data')
                break
    
    finally:
        print("Closing current connection")
        connection.close()