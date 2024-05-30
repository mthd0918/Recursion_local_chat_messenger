import socket
import sys

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = '/tmp/socket_file'
print('connecting to {}'.format(server_address))

# server.pyのプロセスへ接続
try:
    sock.connect(server_address)
except socket.error as e:
    print('connection error: {}'.format(e))
    sys.exit(1)

# メッセージの送信と終了
try:
    # データの受け取り、エンコード、タイムアウトの設定
    country_code = input("Select Country Code(us/jp/it): ").strip().lower()
    while country_code not in ['us', 'jp', 'it']:
        print("Invalid value. Select 'us' or 'jp' or 'it.")
        country_code = input("Select Country Code(us/jp/it): ").strip().lower()
    country_code_bytes = country_code.encode('utf-8')
    sock.sendall(country_code_bytes)
    sock.settimeout(5)
    # データの受け取りと表示、タイムアウト時の処理
    try:
        while True:
            data = sock.recv(1024)
            decode_data = data.decode('utf-8')
            if data:
                print(decode_data)
            else:
                break
    except(TimeoutError):
        print('Socket timeout, ending listening for server message')
finally:
    print('closing socket')
    sock.close()