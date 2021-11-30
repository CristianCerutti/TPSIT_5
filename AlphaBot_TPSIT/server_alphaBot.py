import socket as sck
import AlphaBot
import sqlite3

s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)
s.bind(('0.0.0.0', 11000))
s.listen()
conn, addr = s.accept()
bot = AlphaBot.AlphaBot()                                         #instanza classe AlphaBot
con = sqlite3.connect("db_movimenti.db")
cur = con.cursor()                                                #creazione oggetto cursore            
while True:                                                         
    mess = conn.recv(4096).decode()                               #ricevo i dati dal client
    cont = -1
    for row in cur.execute("SELECT * FROM movimento").fetchall(): #per ogni riga nella tabella movimento (presa tutta)
        if row[0] == mess:                                        #row[0] contiene i comandi come messaggi, row[1] contiene i comandi con il tempo di esecuzione
            lista_comandi = row[1].split(",")                     #split per dividere comando e tempo 
    for comando in lista_comandi:                                 #lista comandi contiene tutti i comandi e i tempi, la si scorre prendendo ogni comando e tempo e eseguendolo singolarmente
        cont += 1
        if comando == "w":
            bot.time_forward(lista_comandi[cont+1])               #cont+1 serve a prendere il tempo del relativo comando
            print("avanti")                                       #in quanto il tempo relativo al comando si trova alla posizione successiva
        if comando.lower() == "s":
            bot.time_backward(lista_comandi[cont+1])
            print("indietro")
        if comando.lower() == "d":
            bot.time_right(lista_comandi[cont+1])
            print("destra")
        if comando.lower() == "a":
            bot.time_left(lista_comandi[cont+1])
            print("sinistra")
s.close()                                                         #chiusura socket e cursore
cur.close()