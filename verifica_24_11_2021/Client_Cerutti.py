import socket as sck
import datetime as dt
import time

s = sck.socket(sck.AF_INET, sck.SOCK_STREAM)    #creazione socket tcp
s.connect((('localhost'), 8000))       #connessione al server
year = 2021
while True:
    month = int(input("inserire il mese: ")) #chiede data
    day = int(input("inserire il giorno: ")) 
    livello = input("inserire il livello") #chiede livello misurato
    id_stazione = input("inserire una id_stazione: ")    #chiede id_stazione' dove è stata effettuata la misura
    s.sendto((str(dt.date(year,month,day))+ "," + str(livello) + "," + str(id_stazione)).encode(), ("localhost",7000))        #tupla con (data, livello_misurato, id_stazione')
    #time.sleep(15)   #aspetta 15 secondi
    mess = s.recvfrom(4096) #aspetta di ricevere il messaggio dal server, di corretta avvenuta operazione o attivazione sirena
    print(mess)
    if mess == "pericolo imminente, accendere la sirena":
        print("pericolo rilevato, accensione sirena")   #avvia la sirena