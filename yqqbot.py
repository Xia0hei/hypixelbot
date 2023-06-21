import socket
import threading
import json

BUFFER_SIZE = 1048576

ADDRESS_SEND = ('127.0.0.1', 5700)
ADDRESS_RECV = ('', 5701)

BOT_LOADER = None


def set_loader(loader):
    global BOT_LOADER
    BOT_LOADER = loader


def _recv_all(sock):
    buffer = b''
    while True:
        data = sock.recv(BUFFER_SIZE)
        buffer += data
        if len(data) != BUFFER_SIZE:
            break
    return buffer


class HttpRequest:

    def __init__(self, method='GET', url='/', headers=None, data=b''):
        self.method = method
        self.url = url
        self.headers = {} if headers is None else headers
        self.data = data

    def set_method(self, method):
        self.method = method
        return self

    def set_url(self, url):
        self.url = url
        return self

    def set_header(self, key, value):
        self.headers[key] = value
        return self

    def set_data(self, data):
        self.data = data
        return self

    def get_header(self, key):
        return self.headers.get(key, None)

    def to_bytes(self):
        lines = []
        lines.append(f'{self.method} {self.url} HTTP/1.1')
        for key, value in self.headers.items():
            lines.append(f'{key}: {value}')
        lines.append('')
        lines.append('')
        return '\r\n'.join(lines).encode('utf-8') + self.data

    @classmethod
    def from_bytes(cls, data):
        request = HttpRequest()
        data, request.data = data.split(b'\r\n\r\n', 1)
        line, *headers = data.decode('utf-8').split('\r\n')
        request.method, request.url, *_ = line.split(' ')
        for header in headers:
            key, value = header.split(':', 1)
            request.set_header(key.strip(), value.strip())
        return request

    @staticmethod
    def encode(string):
        if isinstance(string, str):
            string = string.encode('utf-8')
        return ''.join('%%%02X' % x for x in string)


class HttpResponse:

    def __init__(self, status=200, description='OK', headers=None, data=b''):
        self.status = status
        self.description = description
        self.headers = {} if headers is None else headers
        self.data = data

    def set_status(self, status):
        self.status = status
        return self

    def set_description(self, description):
        self.description = description
        return self

    def set_header(self, key, value):
        self.headers[key] = value
        return self

    def set_data(self, data):
        self.data = data
        return self

    def get_header(self, key):
        return self.headers.get(key, None)

    def to_bytes(self):
        lines = []
        lines.append(f'HTTP/1.1 {self.status} {self.description}')
        for key, value in self.headers.items():
            lines.append(f'{key}: {value}')
        lines.append('')
        lines.append('')
        return '\r\n'.join(lines).encode('utf-8') + self.data

    @classmethod
    def from_bytes(cls, data):
        response = HttpResponse()
        data, response.data = data.split(b'\r\n\r\n', 1)
        line, *headers = data.decode('utf-8').split('\r\n')
        _, response.status, response.description = line.split(' ')
        response.status = int(response.status)
        for header in headers:
            key, value = header.split(':', 1)
            response.set_header(key.strip(), value.strip())
        return response


class HttpClient:

    def __init__(self, request=None):
        self.request = HttpRequest() if request is None else request
        self.response = None

    def connect(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        sock.sendall(self.request.to_bytes())
        response = HttpResponse.from_bytes(_recv_all(sock))
        sock.close()
        return response


class HttpServer:

    def __init__(self, address, backlog=5, processor=None):
        self.address = address
        self.backlog = backlog
        self.processor = self.process if processor is None else processor
        self.thread = None
        self.started = False

    def process(self, request, response):
        pass

    def _accept(self, sock, address):
        request = HttpRequest.from_bytes(_recv_all(sock))
        response = HttpResponse()
        self.processor(request, response)
        sock.sendall(response.to_bytes())
        sock.close()

    def _run(self):
        try:
            self.started = True
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(self.address)
            sock.listen(self.backlog)
            while True:
                client, address = sock.accept()
                thread = threading.Thread(
                    target=self._accept, args=(client, address))
                thread.daemon = True
                thread.start()
        except Exception as e:
            print(e)
        self.started = False

    def start(self, block=False):
        if not self.started:
            if block:
                self._run()
            else:
                self.thread = threading.Thread(target=self._run)
                self.thread.daemon = True
                self.thread.start()


def _send(url):
    client = HttpClient(HttpRequest(url=url))
    client.request.set_header('Host', f'{ADDRESS_SEND[0]}:{ADDRESS_SEND[1]}')
    client.connect(ADDRESS_SEND)


def send_private(number, message):
    _send(
        f'/send_private_msg?user_id={number}&message={HttpRequest.encode(message)}')


def send_group(number, message):
    _send(
        f'/send_group_msg?group_id={number}&message={HttpRequest.encode(message)}')


def _processor(processor):
    def _(request, response):
        try:
            message = json.loads(request.data.decode('utf-8'))
            processor(message)
        except Exception:
            pass
    return _


def start_listener(processor, block=False):
    HttpServer(ADDRESS_RECV, processor=_processor(processor)).start(block)
