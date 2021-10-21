import pprint
import socket
import ssl

# ? Test URL
# url = "http://example.org/index.html"

def request(url):
    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP,
    )

    # Scheme = http, or https
    scheme, url = url.split("://", 1)
    hostname = url.split("/", 1)[0]
    print(hostname)
    assert scheme in ["http", "https"], \
        "Unknown scheme {}".format(scheme)
    port = 80 if scheme == "http" else 443

    host = url.split("/", 1)[0]
    path = ""

    if len(url.split("/", 1)) == 2:
        __, path = url.split("/", 1)
        path = "/" + path
    
    # Wrapping the initial socket connection for SSL, this same "s" variable will be used for a connection.
    if scheme == "https":
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=host)

    if ":" in host:
        host, port = host.split(":", 1)
        hostname = host
        port = int(port)

    print({
        "hostname": hostname,
        "host": host,
        "path": path if path else "",
        "url": url,
        "port": port,
        "scheme": scheme
          })
    s.connect((hostname, port))
    # Implementing the "b" before the string specifies that there are bytes of information being sent, instead of the raw text.
    # This send request returns back to us "47" which represent the amount of bytes.
    rOpt1 = f"GET / HTTP/1.0\r\n"
    rOpt2 = f'Host: {hostname}\r\n\r\n'
    rOpt3 = f'Connection: close\r\n'
    rOpt4 = f'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:50.0) Gecko/20100101 Firefox/50.0'
    options = rOpt1 + rOpt2 + rOpt3 + rOpt4
    print(options)
    print("Sent Bytes:",
          s.send(
              options.encode()
          ))

    # makefile returns a file-like object containing every byte receieved from the server. Turning those bytes into a string using utf8 encoding. Also removing HTTP's weird line endings.
    response = s.makefile("r", encoding="utf8", newline="\r\n")
    statusline = response.readline()
    #print("statusline", statusline)
    version, status, explanation = statusline.split(" ", 2)
    assert status == "200", "{}:{}".format(status, explanation)
    # print({"version": version, "status": status, "explanation": explanation})
    headers = {}
    while True:
        line = response.readline()
        if line == "\r\n":
            break
        # print(line)
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip()
    print(headers)

    body = response.read()
    s.close()
    return headers, body

def displayBody(body):
    # print(body)
    # Print info between the <> brackets in the response body.
    bodyParsed = []

    in_angle = False
    for c in body:
        if c == "<" or c == "{":
            in_angle = True
        elif c == ">" or c == "}":
            in_angle = False
        elif not in_angle:
            bodyParsed.append(c)
            # print(c,end="")
        # print(c, end="")
    
    print(''.join(bodyParsed))

def load(url):
    headers, body = request(url)
    # print(headers)
    displayBody(body)

# ? Test Load
# load(url)

# ? Mimic a main function that will execute from the command line, this will allow the execution of this script with a URL passed in as an arg.
if __name__ == "__main__":
    import sys
    if sys.argv[1]:
        load(sys.argv[1])