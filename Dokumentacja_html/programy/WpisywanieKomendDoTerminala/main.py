import psycopg2
try:
    con = psycopg2.connect("dbname='adam' user='adam' password='zaq123edcxsw'")
    print("Udalo sie polaczyc")
except:
    print("NIe pyklo")
cur = con.cursor()

plik = open('tabelka_szablony.txt', 'r')
line = plik.readline(0)
liczba = 1
for line in plik:
    cur.execute(line)
    con.commit();
    print(liczba, ". Udalo sie")
    liczba+= 1
print("KONIEC")
