import psycopg2
 
constr = "host='localhost' port=5432 dbname=shop user=postgres password='a'"
conn = psycopg2.connect(constr)
cur = conn.cursor()
cur.execute('SELECT shoku_id, hin_mei, syoku_zai, syu3_hin, sei_url FROM shokuhin WHERE shoku_id = shoku_num')
res = cur.fetchall()
print(res)
cur.close()
conn.close()