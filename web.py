import socket
s = socket.socket(
    family=socket.AF_INET,
    type=socket.SOCK_STREAM,
    proto=socket.IPPROTO_TCP,
)

url = "http://example.org/index.html"

assert url.startswith("http://")
url = url[len("http://"):]
host, path = url.split("/", 1)
path = "/" + path
print(host,path)

s.connect(("example.org", 80))
print(s.send(b"GET /index.html HTTP/1.0\r\n" + b"Host: example.org\r\n\r\n"))
