#nome unico 
#client ha il proprio ip address
#invia un messaggio di hello con nick e automaticamente ip
import socket as sck

s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)     #socket UDP/IPv4
#f"nickname:{nick_name}"
nick_name = "Cristian"
hello = f"Nickname:{nick_name}"
s.sendto(hello.encode(),('192.168.88.92', 5000))
ok_resp = s.recvfrom()
#while True:
    #messaggi    
s.close()