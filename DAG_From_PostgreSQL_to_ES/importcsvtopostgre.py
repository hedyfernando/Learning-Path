import psycopg2 as db

conn_string="dbname='company' host='localhost' user='postgres' password='cicak'"
conn=db.connect(conn_string)
cur=conn.cursor()


f = open('/home/cicak/folder_data/data_sumber/telco_data.csv', 'r')
next(f) # skip header row
cur.copy_from(f, 'telco_users', sep=',')

conn.commit()
print('Import Sucess')
f.close()