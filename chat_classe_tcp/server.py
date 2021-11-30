import socket as sck
import sqlite3

s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
s.bind(('0.0.0.0', 3000))
s.listen()
registro = {}
 
while True:
    conn, addr = s.accept()
    mess = conn.recv(4096)
    nickname = conn.split(":")
    if (nickname[0] == "nickname"):
        con = sqlite3.connect("registro.db")
        cur = con.cursor() 
        registro[nickname[1]] = addr[0]
        cur.execute(f'insert into utente values("{nickname[1]}", "{addr[0]}","{addr[1]}"')
        print(f"{nickname[1]} e' entrato nella chat")
        s.sendall("OK".encode())
        con.close()
    else:
        mess = conn.recv(4096).split(":", ",")
        con = sqlite3.connect("registro.db")
        cur = con.cursor() 
        for row in cur.execute("SELECT * FROM utente"):
            if row[0] == mess[3]:
                s.sendall(messaggio[1] + ": ")
                print(f"Nickname: {row[0]}, address: {row[1]}, port: {row[2]}")
            else: 
                print("l'utente non esiste")
        con.close()
s.close()
