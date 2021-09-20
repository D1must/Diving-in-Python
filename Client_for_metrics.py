import socket
import time
import bisect


class ClientError(socket.error):
    pass


class Client:
    def __init__(self, host, port, timeout=None):
        self.port = port
        self.host = host

        try:
            self.connection = socket.create_connection(
                (host, port), timeout)
        except socket.error as err:
            raise ClientError("I can't create a connection", err)

    def read(self):
        """method for reading the answer from socket"""
        data = b""
        while not data.endswith(b"\n\n"):  # waiting for \n\n in the endline
            try:
                data += self.connection.recv(1024)
            except socket.error as err:
                raise ClientError("I can't read the data from socket", err)
        raw_data = data.decode('utf-8')  # reforming the data to str
        status, payload = raw_data.split("\n", 1)
        payload = payload.strip()

        if status == 'error':
            raise ClientError('Server provides an error')
        return payload, status

    def put(self, key, value, timestamp=None):
        timestamp = timestamp or int(time.time())
        # отправляем запрос команды put
        try:
            self.connection.sendall(
                f"put {key} {value} {timestamp}\n".encode())
        except socket.error as err:
            raise ClientError('Server provides an error')
        self.read()

    def get(self, key):
        try:
            self.connection.sendall(f"get {key}\n".encode('utf-8'))
        except socket.error as err:
            raise ClientError("I can't send the data", err)

        payload, status = self.read()
        if status != 'ok':
            raise ClientError('Server returns an error')
        data = {}
        if payload == '':
            return data

        try:  # The answer for get
            for row in payload.splitlines():
                key, value, timestamp = row.split()
                if key not in data:
                    data[key] = []
                bisect.insort(data[key], ((int(timestamp), float(value))))
                # data[key].append((int(timestamp), float(value)))
        except Exception as err:
            raise ClientError('Server provides an incorrect data', err)

        return data

    def close(self):
        try:
            self.connection.close()
        except socket.error as err:
            raise ClientError("I can't close connection", err)


# if __name__ == "__main__":
#     client = Client("127.0.0.1", 8888, timeout=5)
#     client.put("test", 0.5, timestamp=1)
#     client.put("test", 2.0, timestamp=2)
#     client.put("test", 0.5, timestamp=3)
#     client.put("load", 3, timestamp=4)
#     client.put("load", 4, timestamp=5)
#     print(client.get("*"))
#
#     client.close()
