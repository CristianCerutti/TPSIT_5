#ip address (noto anche al client)
#memorizzata una tabellina formata da nickname e ip di ogni client (dizionario formato da chiave nome, e ip valore
#quando arriva una presentazione server risponde OK
#messaggi di testo: f"sender: {nickname_mittente}, receiver: {nick_destinatario}, {messaggio}"
import socket as sck
import sqlite3 

registro = {}

s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)     
s.bind(('0.0.0.0', 5000))    
     

while True:
    data, addr = s.recvfrom(4096)
    data = data.decode()
    nickname = data.split(":")
    print(f"nickname:{nickname}")
    if (nickname[0] == "Nickname"):
        con = sqlite3.connect("registro.db")
        cur = con.cursor()  
        registro[nickname[1]] = addr[0]
        cur.execute(f'insert into utente values("{nickname[1]}", "{addr[0]}","{addr[1]}"')
        print(f"{nickname[1]} e' entrato nella chat")
        s.sendto("OK", addr)
        con.close()
    else:
        messaggio = data.split(":", ",")
        con = sqlite3.connect("registro.db")
        cur = con.cursor()  
        for row in cur.execute("SELECT * FROM utente"):
            if row[0] == messaggio[3]:
                s.sendto(messaggio[1]+ ": ")
            print(f"Nickname: {row[0]}, address: {row[1]}, port: {row[2]}")
        #if messaggio[3] in registro:
            #s.sendto(messaggio[1]+ ": "+ messaggio[4], addr[0]) 
s.close()