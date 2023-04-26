import paramiko
import psycopg2
from sshtunnel import SSHTunnelForwarder

try:
    server = SSHTunnelForwarder(('10.71.28.8', 22),
                                ssh_username='adam',
                                ssh_password='zaq123edcxsw',
                                ssh_proxy_enabled=True,
                                remote_bind_address=('localhost', 5432))
    server.start()
    print('Server started')

    con = psycopg2.connect(database='adam',
                           host='localhost',
                           user='adam',
                           password='zaq123edcxsw',
                           port=server.local_bind_port)
    if con != None:
        print('poloaczono')
    else:
        print('Nie polaczaono')

    cursor = con.cursor()
    cursor.execute("SELECT * FROM lekarz WHERE lkz_imiona='TheDoctor';")
    krotka_lekarz1 = cursor.fetchone()
    con.commit()
    print(krotka_lekarz1)
    server.close()

except BaseException as e:
    print('prolem with', e)
finally:
    if server:
        server.close()

try:
    server2 = SSHTunnelForwarder(('10.71.28.17', 22),
                                 ssh_username='adam',
                                 ssh_password='zaq123edcxsw',
                                 ssh_proxy_enabled=True,
                                 remote_bind_address=('localhost', 5432))
    server2.start()
    print('Server2 started')

    con2 = psycopg2.connect(database='adam',
                            host='localhost',
                            user='adam',
                            password='zaq123edcxsw',
                            port=server2.local_bind_port)
    if con2 != None:
        print('poloaczono')
    else:
        print('Nie polaczaono')

    cursor2 = con2.cursor()
    cursor2.execute("SELECT * FROM lekarz1 WHERE lkz_imiona='Piotr';")
    krotka_lekarz2 = cursor2.fetchone()
    con2.commit()
    print(krotka_lekarz2)
    server2.close()

except BaseException as e:
    print('prolem with', e)
finally:
    if server2:
        server2.close()
