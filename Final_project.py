import asyncio
from collections import defaultdict


class Metric_storage:
    """Class for the keeping of metrics in memory"""

    def __init__(self):
        # defaultdict allows us to create keys if they don't find in dict
        self._data = defaultdict(dict)

    def put(self, key, value, timestamp):
        self._data[key][timestamp] = value

    def get(self, key):
        # data = self._data

        # come back needed metric except *
        if key == '*':
            # deepcopy allows us to create dict without changing orliginal dict
            # return copy.deepcopy(self._data)
            return self._data

        if key in self._data:
            return {key: self._data.get(key)}

        return {}


class ClientProtocol:
    """class for working with put and get"""

    def __init__(self, storage):
        self.storage = storage

    def __call__(self, data):

        method, *parametres = data.split()

        if method == "put":
            key, value, timestamp = parametres
            value = float(value)
            timestamp = int(timestamp)
            self.storage.put(key, value, timestamp)
            return {}
        elif method == "get":
            key = parametres.pop()
            if parametres:
                raise ProtocolError
            return self.storage.get(key)
        else:
            raise ProtocolError


# I need to reduct it
class ClientServerProtocol(asyncio.Protocol):
    storage = Metric_storage()
    # settings for answers from server
    endline = '\n'
    error_message = "wrong command"
    code_err = 'error'
    code_ok = 'ok'

    def __init__(self):
        super().__init__()
        self.client = ClientProtocol(self.storage)
        self._buffer = b''

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        """Method data_received recall with giving data in socet"""
        self._buffer += data

        try:
            request = self._buffer.decode()
            # waiting for the data with ends \n
            if not request.endswith(self.endline):
                return

            self._buffer, message = b'', ''
            raw_data = self.client(request.rstrip(self.endline))

            for key, values in raw_data.items():
                message += self.endline.join(f'{key} {value} {timestamp}'
                                             for timestamp, value in sorted(values.items()))
                message += self.endline

            code = self.code_ok
        except (ValueError, UnicodeDecodeError, IndexError):
            message = self.error_message + self.endline
            code = self.code_err

        answer = f'{code}{self.endline}{message}{self.endline}'
        # give answer
        self.transport.write(answer.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


class ProtocolError(ValueError):
    pass

# additional
# if __name__ == "__main__":
#     run_server("127.0.0.1", 8888)
