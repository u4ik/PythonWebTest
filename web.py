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
# Implementing the "b" before the string specifies that there are bytes of information being sent, instead of the raw text.
# This send request returns back to us "47" which are the amount of bytes that we've sent
print(s.send(b"GET /index.html HTTP/1.0\r\n" + b"Host: example.org\r\n\r\n"))

# makefile returns a file-like object containing every byte receieved from the server. Turning those bytes into a string using utf8 encoding. Also removing HTTP's weird line endings.
response = s.makefile("r", encoding="utf8", newline="\r\n")
