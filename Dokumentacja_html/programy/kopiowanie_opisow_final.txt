import paramiko
import psycopg2
from sshtunnel import SSHTunnelForwarder
############################## LACZENIE SIE Z BAZA DANYCH z MASZYNY-B ##########################################################################
try:
    server_maszyna_B = SSHTunnelForwarder(
        ('10.71.28.8', 22),
        ssh_username='adam',
        ssh_password='zaq123edcxsw',
        ssh_proxy_enabled=True,
        remote_bind_address=('localhost', 5432))
    server_maszyna_B.start()

    con_B = psycopg2.connect(database='adam',
                             host='localhost',
                             user='adam',
                             password='zaq123edcxsw',
                             port=server_maszyna_B.local_bind_port)
    if con_B != None:
        print('\nPolaczono z baza danych z Maszyny-B')
    else:
        print('\nBlad - NIe polaczylo z baza danych z Maszyny-B')
        quit()

    cur_B = con_B.cursor()

except BaseException as err:
    print('Problem z', err)
    quit()
############################## LACZENIE SIE Z BAZA DANYCH z MASZYNY-C ##########################################################################
try:
    server_maszyna_C = SSHTunnelForwarder(
        ('10.71.28.17', 22),
        ssh_username='adam',
        ssh_password='zaq123edcxsw',
        ssh_proxy_enabled=True,
        remote_bind_address=('localhost', 5432))
    server_maszyna_C.start()

    con_C = psycopg2.connect(database='adam',
                             host='localhost',
                             user='adam',
                             password='zaq123edcxsw',
                             port=server_maszyna_C.local_bind_port)
    if con_C != None:
        print('Polaczono z baza danych z Maszyny-C\n')
    else:
        print('Blad - NIe polaczylo z baza danych z Maszyny-C\n')
        quit()
    cur_C = con_C.cursor()

except BaseException as err:
    print('Problem z', err)
    quit()


############################## FUNKCJA KTORA SPRAWDZA CZY PODANY LEKARZ JEST POPRAWNY ##########################################################
def poprawny_lekarz():
    global nazwa_lekarza_1
    nazwa_lekarza_1 = input(
        'Podaj imie lekarza z ktorego chcesz skopiowac opis: ')
    cur_B.execute("SELECT * FROM lekarz WHERE lkz_imiona=%s;",
                  (nazwa_lekarza_1, ))
    krotka_lekarz1 = cur_B.fetchone()
    con_B.commit()
    while krotka_lekarz1 == None:
        nazwa_lekarza_1 = input(
            'Podaj POPRAWNE imie lekarza z ktorego chcesz skopiowac opis: ')
        cur_B.execute("SELECT * FROM lekarz WHERE lkz_imiona=%s;",
                      (nazwa_lekarza_1, ))
        krotka_lekarz1 = cur_B.fetchone()
        con_B.commit()
    return krotka_lekarz1

########################### FUNKCJA KTORA PRZYWRACA BAZY DANYCH DO MOMENTU PRZED KOPIOWANIEM (backup) ##################################################
def przywrocenie_backup():
	wybor_4 = input('\nCzy chcesz przywrocic bazy danych (z Maszyny-B i -C) do stanu przed kopiowaniem np. do potestowania innych wartosci? (t - tak, inne - nie): ')
	if wybor_4 == 't' or wybor_4 == 'T':
		cur_C.execute('DROP TABLE szablon_opisu;')
		con_C.commit()
		cur_C.execute('CREATE TABLE szablon_opisu AS SELECT * FROM szablon_opisu_backup;')
		con_C.commit()
		print('Pomyslnie przywrocono szablon_opisu.')

krotka_lekarz1 = poprawny_lekarz()

############################## FUNKCJA KTORA SPRAWDZA CZY PODANY LEKARZ MA JAKIES INFORMACJE W BAZIE DANYCH ####################################
cur_B.execute("SELECT * FROM szablon_opisu WHERE sou_lkz_id=%s;",
              (krotka_lekarz1[0], ))
krotka_czy_sa = cur_B.fetchone()
con_B.commit()
while krotka_czy_sa == None:
    wybor_3 = input(
        '\nPodany lekarz nie ma zadnych informacji w szablon_opisu. Czy chcesz podac innego lekarza? (t - tak, inny klawisz - konczy dzialanie programu): '
    )
    if wybor_3 == 't' or wybor_3 == 'T':
        krotka_lekarz1 = poprawny_lekarz()
        cur_B.execute("SELECT * FROM szablon_opisu WHERE sou_lkz_id=%s;",
                      (krotka_lekarz1[0], ))
        krotka_czy_sa = cur_B.fetchone()
        con_B.commit()
    else:
        print('Koniec')
        quit()

nazwa_lekarza_2 = input(
    '\nPodaj imie lekarza do ktorego chcesz skopiowac opis (Gdy wpiszesz all to skopiuje do wszystkich lekarzy informacje): '
)

################################## FUNKCJA KTORA KOPIUJE DO KAZDEGO LEKARZA Z MASZYNY-C INFORMACJE Z LEKARZA z BAZY DANYCH OD MASZYNY-B ################################
if nazwa_lekarza_2 == 'all':
    id_lekarz_1 = krotka_lekarz1[0]

    cur_B.execute("SELECT * FROM szablon_opisu WHERE sou_lkz_id=%s;",
                  (krotka_lekarz1[0], ))
    kl = cur_B.fetchall()
    con_B.commit()

    cur_C.execute("SELECT * FROM lekarz1")
    krotka_all = cur_C.fetchall()
    con_C.commit()
    w_j = 0
    w_i = 0
    for j in range(0, len(kl)):
        for i in range(0, len(krotka_all)):
            cur_C.execute(
                'INSERT INTO szablon_opisu VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (kl[j][0], kl[j][1], kl[j][2], kl[j][3], kl[j][4], kl[j][5],
                 kl[j][6], krotka_all[i][0], kl[j][8], kl[j][9], kl[j][10]))
            con_C.commit()
            w_i += 1
        w_j += 1
    print('\nSkopiowano', w_j,'informacji do', w_i,'lekarzy')
    przywrocenie_backup()
    print('Koniec')
    quit()

############################### FUNKCJA KTORA KOPIUJE INFORMACJE TYLKO DO JEDNEGO PODANEGO LEKARZA ##############################################
else:
    cur_C.execute("SELECT * FROM lekarz1 WHERE lkz_imiona=%s;", (nazwa_lekarza_2, ))
    krotka_lekarz2 = cur_C.fetchone()
    con_C.commit()
    while krotka_lekarz2 == None:
        nazwa_lekarza_2 = input(
            'Podaj POPRAWNE imie lekarza do ktorego chcesz skopiowac opis: ')
        cur_C.execute("SELECT * FROM lekarz1 WHERE lkz_imiona=%s;",
                      (nazwa_lekarza_2, ))
        krotka_lekarz2 = cur_C.fetchone()
        con_C.commit()

print('\n1=================LEKARZ_1=================1')
print(krotka_lekarz1)
print('2=================LEKARZ_2=================2')
print(krotka_lekarz2)

id_lekarz_1 = krotka_lekarz1[0]
id_lekarz_2 = krotka_lekarz2[0]

############################### FUNKCJA KTORA POKAZUJE INOFRMACJE PRZED KOPIOWANIEM O PODANYM LEKARZU #############################################
print(
    '\n==================================================================================='
)
print('Informacje z szablonu opisu lekarza o imieniu ', nazwa_lekarza_2,
      ' przed kopiowaniem z Maszyny-C: ')
cur_C.execute("SELECT * FROM szablon_opisu WHERE sou_lkz_id=%s;",
              (id_lekarz_2, ))
krotka_przed_kopiowaniem_lekarz2 = cur_C.fetchall()
con_C.commit()
if krotka_przed_kopiowaniem_lekarz2 == None or krotka_przed_kopiowaniem_lekarz2 == []:
    print('Brak informacji w Maszynie-C o podanym lekarzu')
else:
    print(krotka_przed_kopiowaniem_lekarz2)

############################### FUNKCJA KTORA KOPIUJE WSZYSTKIE INFORMACJE OD LEKARZA MASZYNY-B DO LEKARZA MASZYNY-C##############################
print(
    '\n==================================================================================='
)
print('Kopiuje dane z z szablon_opisu od lekarza ', nazwa_lekarza_1,
      'z Maszyny-B do lekarza ', nazwa_lekarza_2,' z Maszyny-C')
cur_B.execute("SELECT * FROM szablon_opisu WHERE sou_lkz_id=%s;",
              (krotka_lekarz1[0], ))
kl = cur_B.fetchall()
con_B.commit()
for j in range(0, len(kl)):
    cur_C.execute(
        'INSERT INTO szablon_opisu VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
        (kl[j][0], kl[j][1], kl[j][2], kl[j][3], kl[j][4], kl[j][5], kl[j][6],
         id_lekarz_2, kl[j][8], kl[j][9], kl[j][10]))
    con_C.commit()
    print('Skopiowano tyle danych: ', j)

############################# FUNKCJA KTORA PYTA SIE O POKAZANIE WYNIKU KOPIOWANIA ################################################################
print(
    '\n==================================================================================='
)
wybor_2 = input(
    "Czy chcesz zobaczysz wynik PO kopiowaniu na Maszynie-C? Uwaga może to zawalic cały terminal: (t - tak, inny klawisz - nie)"
)
if wybor_2 == 't' or wybor_2 == 'T':
    print('Informacje z szablonu opisu lekarza o imieniu ', nazwa_lekarza_2,
          ' po kopiowaniu: ')
    cur_C.execute("SELECT * FROM szablon_opisu WHERE sou_lkz_id=%s;",
                  (id_lekarz_2, ))
    print(cur_C.fetchall())
    con_C.commit()
    
############################# PRZYWROCENIE BAZ DANYCH DO MOMENTU PRZED KOPIOWANIEM (backup) ################################################
przywrocenie_backup()
	
server_maszyna_B.stop()
server_maszyna_C.stop()
print('Koniec')
