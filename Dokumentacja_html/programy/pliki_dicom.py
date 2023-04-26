import os.path, time, os
sciezka_zrodlowa = input('Podaj sciezke do plikow DICOM rozpakowanych (np. /home/adam/Pobrane/di): \n')
sciezka_docelowa = input('Podaj sciezke do ktorej mam przekopiowac posortowane pliki DICOM  (np. /home/adam/Pobrane/posortowane i podaj razem z nowym folderem ktory ma miec te pliki \n): ')
while sciezka_docelowa == sciezka_zrodlowa:
	sciezka_docelowa = input('Folder docelowy nie moze byc taki sam jak zrodlowy. Podaj inny  (np. /home/adam/Pobrane/posortowane i podaj razem z nowym folderem ktory ma miec te pliki \n): ')

wybor_1 = input('Chcesz zeby sortowac po dacie modyfikacji czy dacie stworzenia pliku? (m - mody, s - stworz)')
while wybor_1 != 'm' and wybor_1 != 's'and wybor_1 != 'M' and wybor_1 != 'S' :
	wybor_1 = input('Podaj poprawna opcje. (m - mody, s - stworz)')

mkdir = 'mkdir -p '
n_p_d = 'a' #n_p_d = nazwa_pliku_dicom
nazwa_accnum = 'a'

for nazwa_folderu_1 in os.listdir(sciezka_zrodlowa):
    podkatalog_folderu_1 = os.path.join(sciezka_zrodlowa, nazwa_folderu_1)
    for podkatalog_folderu_2 in os.listdir(podkatalog_folderu_1):
    	nazwa_accnum = os.path.join(podkatalog_folderu_1, podkatalog_folderu_2)
    	
    	if nazwa_accnum == 'MD5SUM': ##Usuwa ten plik zeby nie wywalal blad
    		rm = 'rm ' + nazwa_accnum
    		os.system(rmdir)
    		
    	for pliki_dicom in os.listdir(nazwa_accnum):
    		n_p_d = os.path.join(nazwa_accnum, pliki_dicom)
    		
    		if wybor_1 == 'm' or wybor_1 == 'M':
    			data = time.ctime(os.path.getmtime(n_p_d))
    		else:
    			data = time.ctime(os.path.getctime(n_p_d))
    		
    		final_com = sciezka_docelowa + '/' + data[(len(data)-4):] + '/' + data[4:7] + '/' + data[0:3] + '/' + data[11:19] + '/' + nazwa_accnum[(len(nazwa_accnum)-8):len(nazwa_accnum)]
    		os.system(mkdir+final_com)
    		cp = 'cp ' + n_p_d + ' ' + final_com
    		os.system(cp)
print('Zrobione!')

