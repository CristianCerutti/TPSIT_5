import threading
import socket as sck
import datetime as dt
import time
import logging
import sqlite3

def thread_function(mess, address,port,s):      #funzione che viene eseguita dal thread
    con = sqlite3.connect("C:/Users/crice/Desktop/fiumi.db") #connessione con il database
    cur = con.cursor()  #creazione oggetto cursore sulla connessione precedentemente creata
    print(mess)
    dati = mess.split(",")      #dati[0] = data inviata, dati[1] = livello misurato, dati[2] = id_stazione
    print(dati)
    data_misurazione = dati[0]
    livello = dati[1]
    id_stazione = dati[2]
    trovato = False
    for row in cur.execute("SELECT * FROM livelli"):    #cerco nel database l'id_stazione, fetchall mi "ritorna" la tabella creata dalla query
        print(row)
        if int(row[0]) == int(id_stazione):   #row[0] = id_stazione, row[1] = fiume, row[2] = localita, row[3] = livello
            trovato = True
            if int(livello) < int(row[3] - row[3] * 30 / 100):    #livello inferiore al 30%
                s.sendto("ricezione correttamente avvenuta".encode(), (address,port))
            elif int(livello) >= int(row[3] - row[3] * 30 / 100) and int(livello < row[3] - row[3] * 70 / 100):    #livello superiore al 30%, ma inferiore al 70%
                s.sendto("ricezione correttamente avvenuta".encode(), (addrress,port))
                print(f"pericolo sulla stazione di {row[2]}, fiume: {row[1]}, in data: {dati[0]}, valore supera il 30% ma inferiore al 70%") #stampa sulla console del server
            elif  int(livello) >= int(row[3] - row[3] * 70 / 100):        #livello superiore al 70%
                s.sendto("pericolo imminente, accendere la sirena".encode(), (address,port))
                print(f"pericolo sulla stazione di {row[2]}, fiume: {row[1]}, in data: {dati[0]}, il valore super il 70%") #stampa sulla console del server
    if trovato == False:
        print("messaggio ricevuto errato") #stampa sulla console del server
        s.sendto(b"messaggio ricevuto errato", (address,port)) 

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_STREAM) #creazione socket
    s.bind(('localhost', 8000)) #selezione porta e indirizzo ip sui quali "girerà" il socket
    s.listen() #si mette in ascolto di possibili client
    threads = []
    while True:  
        conn, addr = s.accept()  #accetta la connessione
        address = addr[0]  
        port = addr[1]                                                    
        mess = conn.recv(4096).decode() #ricezione messaggio
        x = threading.Thread(target=thread_function(mess,address,port,conn),daemon=True) #creo il thread
        threads.append(x) #lo aggiungo alla lista di thread
        x.start()   #faccio partire il thread
        for thread in threads:  #chiusura di tutti i thread aperti
            thread.join()   #chiudo il thread con la join()

if __name__ == "__main__":
    main()
    