import socket as sck

s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
s.connect((('localhost'), 3000))
nick_name = "Cristian"
hello = f"Nickname:{nick_name}"
while True:
    s.sendall(hello.encode())
    ok_resp = s.recv(4096)
s.close()