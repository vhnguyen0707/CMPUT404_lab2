#!/usr/bin/env python3
import socket, time, sys
from weakref import proxy

#define global address and buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

# get ip
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    print(f'IP address of {host} is {remote_ip}')
    return remote_ip

def main():
    host = 'www.google.com'
    port = 80

    # create socket
    # act as a server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
        print("Starting proxy server")
        # allow reused addresses, bind, and set to listening mode
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen()

        while True:
            # connect proxy_start
            conn, addr = proxy_start.accept()
            print("Connected by", addr)

            # act as a client -> send data from client to server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                print("Connecting to Google")
                remote_ip = get_remote_ip(host)

                # connect to Google at http port
                proxy_end.connect((remote_ip, port))

                send_full_data = conn.recv(BUFFER_SIZE)  # get data from client
                print(f"Sending received data {send_full_data} to google")
                proxy_end.sendall(send_full_data) # then send to google
                proxy_end.shutdown(socket.SHUT_WR)

                data = proxy_end.recv(BUFFER_SIZE) # get data from google
                print(f'Sending received data {data} to client')
                conn.send(data) # send data to client
            conn.close()

if __name__ == "__main__":
    main()