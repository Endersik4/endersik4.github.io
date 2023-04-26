import psycopg2

def poprawny_lekarz():
	global nazwa_lekarza_1
	nazwa_lekarza_1 = input('Podaj imie lekarza z ktorego chcesz skopiowac opis: ')
	cur.execute("SELECT * FROM lekarz WHERE lkz_imiona=%s;", (nazwa_lekarza_1,))
	krotka_lekarz1 = cur.fetchone()
	conn.commit()
	while krotka_lekarz1 == None:
		nazwa_lekarza_1 = input('Podaj POPRAWNE imie lekarza z ktorego chcesz skopiowac opis: ')
		cur.execute("SELECT * FROM lekarz WHERE lkz_imiona=%s;", (nazwa_lekarza_1,))
		krotka_lekarz1 = cur.fetchone()
		conn.commit()
	return krotka_lekarz1
try:
	conn = psycopg2.connect("dbname='adam' user='adam' password='zaq123edcxsw'")
	print("Udalo sie polaczyc z baza danych")
except:
	print("Nie pyklo!")

cur = conn.cursor()

krotka_lekarz1 = poprawny_lekarz()

cur.execute("SELECT * FROM szablon_opisu2 WHERE sou_lkz_id=%s;", (krotka_lekarz1[0],))
krotka_czy_sa = cur.fetchone()
conn.commit()
while krotka_czy_sa == None:
	if krotka_czy_sa == None:
		wybor_3 = input('Podany lekarz nie ma zadnych informacji w szablon_opisu. Czy chcesz podac innego lekarza? (t - tak, inny klawisz - konczy dzialanie programu): ')
		if wybor_3 == 't' or wybor_3 == 'T':
			krotka_lekarz1 = poprawny_lekarz()
			cur.execute("SELECT * FROM szablon_opisu2 WHERE sou_lkz_id=%s;", 	(krotka_lekarz1[0],))
			krotka_czy_sa = cur.fetchone()
			conn.commit()
		else:
			print('Koniec')
			quit()


nazwa_lekarza_2 = input('Podaj imie lekarza do ktorego chcesz skopiowac opis (Gdy wpiszesz all to skopiuje do wszystkich lekarzy informacje): ')
if nazwa_lekarza_2 == 'all':
	id_lekarz_1 = krotka_lekarz1[0]

	cur.execute("SELECT * FROM szablon_opisu2 WHERE sou_lkz_id=%s;", (krotka_lekarz1[0],))
	kl = cur.fetchall()
	conn.commit()

	cur.execute("SELECT * FROM lekarz2")
	krotka_all = cur.fetchall()
	conn.commit()
	for j in range(0, len(kl)):
		for i in range(0, len(krotka_all)):	
			cur.execute('INSERT INTO szablon_opisu3 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (kl[j][0], kl[j][1], kl[j][2], kl[j][3], kl[j][4], kl[j][5], kl[j][6], krotka_all[i][0], kl[j][8], kl[j][9], kl[j][10]))
			conn.commit()
			print('Zrobiono - i = ',i, ' j =',j)
	print('Koniec')
	quit()
else:
	cur.execute("SELECT * FROM lekarz2 WHERE lkz_imiona=%s;", (nazwa_lekarza_2,))
	krotka_lekarz2 = cur.fetchone()
	conn.commit()
	while krotka_lekarz2 == None:
		nazwa_lekarza_2 = input('Podaj POPRAWNE imie lekarza do ktorego chcesz skopiowac opis: ')
		cur.execute("SELECT * FROM lekarz2 WHERE lkz_imiona=%s;", (nazwa_lekarza_2,))
		krotka_lekarz2 = cur.fetchone()
		conn.commit()

print('1=================LEKARZ_1=================1')
print(krotka_lekarz1)
print('2=================LEKARZ_2=================2')
print(krotka_lekarz2)

id_lekarz_1 = krotka_lekarz1[0]
id_lekarz_2 = krotka_lekarz2[0]

print('===================================================================================')
print('Informacje z szablonu opisu lekarza o imieniu ', nazwa_lekarza_2,' przed kopiowaniem: ')
cur.execute("SELECT * FROM szablon_opisu2 WHERE sou_lkz_id=%s;", (id_lekarz_2,))
krotka_przed_kopiowaniem_lekarz2 = cur.fetchall()
conn.commit()
if krotka_przed_kopiowaniem_lekarz2 == None or krotka_przed_kopiowaniem_lekarz2 == []:
	print('Brak informacji')
else:
	print(krotka_przed_kopiowaniem_lekarz2)

print('===================================================================================')
print('Kopiuje dane z z szablon_opisu od lekarza ', nazwa_lekarza_1,' do lekarza ', nazwa_lekarza_2)
cur.execute("SELECT * FROM szablon_opisu2 WHERE sou_lkz_id=%s;", (krotka_lekarz1[0],))
kl = cur.fetchall()
conn.commit()
for j in range(0, len(kl)):	
	cur.execute('INSERT INTO szablon_opisu3 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', (kl[j][0], kl[j][1], kl[j][2], kl[j][3], kl[j][4], kl[j][5], kl[j][6], id_lekarz_2, kl[j][8], kl[j][9], kl[j][10]))
	conn.commit()
	print('Zrobiono - j =',j)

print('===================================================================================')
wybor_2 = input("Czy chcesz zobaczysz wynik PO kopiowaniu? Uwaga może to zawalic cały terminal: (t - tak, inny klawisz - nie)")
if wybor_2 == 't' or wybor_2 == 'T':
	print('Informacje z szablonu opisu lekarza o imieniu ', nazwa_lekarza_2,' po kopiowaniu: ')
	cur.execute("SELECT * FROM szablon_opisu3 WHERE sou_lkz_id=%s;", (id_lekarz_2,))
	print(cur.fetchall())
	conn.commit()
else:
	print('Koniec.')




