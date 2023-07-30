import socket
import threading
import select
import socks


SOCKS_VERSION = 5

class PuddingProxy :

    def __init__(self, address:str, port:int, username:str=None, password:str=None) :
        '''
        ### Creates a local host proxy without authentication, which is chained to a remote proxy.
        
        ---

        * address => the socks5 ip address

        * port => the socks port

        * username => the username

        * password => the password
        '''
        self.address = address
        self.port = port
        self.username = username
        self.password = password
        self.server_socket = None
        self.client_connections = []

    def launch(self) :
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('', 0))
        threading.Thread(target=self.listen, daemon=True).start()
        self.local_address, self.local_port = self.server_socket.getsockname()
        return self.local_address, self.local_port

    
    def handle_client(self, connection):
        try :
            # greeting header
            # read and unpack 2 bytes from a client
            version, nmethods = connection.recv(2)

            # get available methods [0, 1, 2]
            methods = self.get_available_methods(nmethods, connection)

            # accept only NO AUTHENTICATION REQUIRED method
            if 0 not in set(methods):
                # close connection
                connection.close()
                return

            # send welcome message
            connection.sendall(bytes([SOCKS_VERSION, 0]))

            # request (version=5)
            version, cmd, _, address_type = connection.recv(4)

            if address_type == 1:  # IPv4
                address = socket.inet_ntoa(connection.recv(4))
            elif address_type == 3:  # Domain name
                domain_length = connection.recv(1)[0]
                address = connection.recv(domain_length)
                address = socket.gethostbyname(address)

            # convert bytes to unsigned short array
            port = int.from_bytes(connection.recv(2), 'big', signed=False)

            try:
                if cmd == 1:  # CONNECT
                    remote = socks.socksocket()  # create a socket object
                    remote.set_proxy(
                        proxy_type=socks.PROXY_TYPE_SOCKS5,
                        addr=self.address,
                        port=self.port,
                        username=self.username,
                        password=self.password
                    )  # set the proxy info
                    remote.connect((address, port))  # connect to the remote proxy
                    bind_address = remote.getsockname()
                else:
                    connection.close()

                addr = int.from_bytes(socket.inet_aton(bind_address[0]), 'big', signed=False)
                port = bind_address[1]

                reply = b''.join([
                    SOCKS_VERSION.to_bytes(1, 'big'),
                    int(0).to_bytes(1, 'big'),
                    int(0).to_bytes(1, 'big'),
                    int(1).to_bytes(1, 'big'),
                    addr.to_bytes(4, 'big'),
                    port.to_bytes(2, 'big')
                ])
            except Exception as e:
                # return connection refused error
                reply = self.generate_failed_reply(address_type, 5)

            connection.sendall(reply)

            # establish data exchange
            if reply[1] == 0 and cmd == 1:
                self.exchange_loop(connection, remote)

            connection.close()
        except :
            pass

    def exchange_loop(self, client, remote):
        while True:
            # wait until client or remote is available for read
            r, w, e = select.select([client, remote], [], [])

            if client in r:
                data = client.recv(4096)
                if remote.send(data) <= 0:
                    break

            if remote in r:
                data = remote.recv(4096)
                if client.send(data) <= 0:
                    break

    def generate_failed_reply(self, address_type, error_number):
        return b''.join([
            SOCKS_VERSION.to_bytes(1, 'big'),
            error_number.to_bytes(1, 'big'),
            int(0).to_bytes(1, 'big'),
            address_type.to_bytes(1, 'big'),
            int(0).to_bytes(4, 'big'),
            int(0).to_bytes(4, 'big')
        ])

    def get_available_methods(self, nmethods, connection):
        methods = []
        for i in range(nmethods):
            methods.append(ord(connection.recv(1)))
        return methods
    
    def listen(self):
        self.server_socket.listen()

        while True:
            if self.server_socket.fileno() == -1:  # The socket has been closed
                break
            conn, addr = self.server_socket.accept()
            self.client_connections.append(conn)
            threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def kill(self):
        for conn in self.client_connections:
            try: conn.close()
            except: pass
        try: self.server_socket.close()
        except: pass